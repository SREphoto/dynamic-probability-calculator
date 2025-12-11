
import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Import custom modules
try:
    from modules import probability, distributions, simulations, statistics, scenarios
except ImportError as e:
    st.error(f"Error import modules: {e}")
    st.stop()

from utils import validate_input, format_probability

def load_css():
    try:
        with open(".streamlit/custom.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass

def render_probability_tab():
    st.header("Classical Probability Logic")
    calc_type = st.selectbox(
        "Select Calculation",,
        ["Joint Probability (AND)", "Union Probability (OR)", "Conditional Probability", "Bayesian Inference", "Expected Value"]
    )
    
    variables = {}
    result = None

    if calc_type in ["Joint Probability (AND)", "Union Probability (OR)"]:
        st.info("Add independent events and their probabilities.")
        if 'variables' not in st.session_state: st.session_state.variables = [{'name': 'Event A', 'value': 0.5}]
        
        col1, col2 = st.columns(2)
        if col1.button("Add Variable ➕"):
            st.session_state.variables.append({'name': f'Event {len(st.session_state.variables)+1}', 'value': 0.5})
        if col2.button("Clear 🗑️"):
            st.session_state.variables = [{'name': 'Event A', 'value': 0.5}]

        for i, var in enumerate(st.session_state.variables):
            c1, c2, c3 = st.columns([3, 3, 1])
            var['name'] = c1.text_input(f"Name {i+1}", var['name'], key=f"p_name_{i}")
            var['value'] = c2.number_input(f"Prob {i+1}", 0.0, 1.0, var['value'], step=0.01, key=f"p_val_{i}")
            if len(st.session_state.variables) > 1 and c3.button("❌", key=f"p_del_{i}"):
                st.session_state.variables.pop(i)
                st.rerun()
            variables[var['name']] = var['value']

        if st.button("Calculate"):
            if calc_type == "Joint Probability (AND)":
                result = probability.calculate_joint_probability(variables)
            else:
                result = probability.calculate_union_probability(variables)
    
    elif calc_type == "Conditional Probability":
        c1, c2 = st.columns(2)
        event_A = c1.text_input("Event A (Given)", "Rain")
        p_a = c1.number_input(f"P({event_A})", 0.0001, 1.0, 0.3)
        event_B = c2.text_input("Event B (Target)", "Traffic")
        
        mode = st.radio("Input Mode", ["Intersection", "Independent"])
        intersection_prob = None
        if mode == "Intersection":
            intersection_prob = st.number_input(f"P({event_A} ∩ {event_B})", 0.0, 1.0, 0.1)
            variables = {event_A: p_a}
        else:
            p_b = c2.number_input(f"P({event_B})", 0.0, 1.0, 0.5)
            variables = {event_A: p_a, event_B: p_b}

        if st.button("Calculate"):
            try:
                result = probability.calculate_conditional_probability(variables, event_A, event_B, intersection_prob)
            except ValueError as e:
                st.error(e)

    elif calc_type == "Bayesian Inference":
        c1, c2 = st.columns(2)
        h = c1.text_input("Hypothesis (H)", "Disease")
        p_h = c1.number_input(f"Prior P({h})", 0.0, 1.0, 0.01)
        e = c2.text_input("Evidence (E)", "Positive Test")
        p_e = c2.number_input(f"Marginal P({e})", 0.0, 1.0, 0.05)
        p_e_given_h = st.number_input(f"Likelihood P({e}|{h})", 0.0, 1.0, 0.95)
        
        variables = {h: p_h, e: p_e, f"P({e}|{h})": p_e_given_h}
        if st.button("Calculate"):
             try:
                result = probability.calculate_bayesian_inference(variables, h, e)
             except ValueError as e:
                st.error(e)

    elif calc_type == "Expected Value":
        if 'ev_data' not in st.session_state:
            st.session_state.ev_data = pd.DataFrame({'Outcome': [1.0, 2.0, 3.0], 'Probability': [0.2, 0.3, 0.5]})
        st.session_state.ev_data = st.data_editor(st.session_state.ev_data, num_rows="dynamic")
        
        if st.button("Calculate"):
            vars_ev = {}
            for _, row in st.session_state.ev_data.iterrows():
                try:
                    vars_ev[str(float(row['Outcome']))] = float(row['Probability'])
                except:
                    pass
            try:
                result = probability.calculate_expected_value(vars_ev)
            except ValueError as e:
                st.error(e)

    if result is not None:
        st.success(f"Result: {format_probability(result)}")

def render_distributions_tab():
    st.header("Probability Distributions")
    dist_type = st.selectbox("Select Distribution", ["Binomial", "Poisson", "Normal", "Geometric", "Exponential"])
    
    fig = go.Figure()
    
    if dist_type == "Binomial":
        c1, c2, c3 = st.columns(3)
        n = c1.number_input("Trials (n)", 1, 1000, 10)
        p = c2.number_input("Prob (p)", 0.0, 1.0, 0.5)
        k = c3.number_input("Successes (k)", 0, n, 5)
        
        prob = distributions.calculate_binomial_probability(n, k, p)
        st.metric(f"P(X={k})", f"{prob:.4f}")
        
        # Plot
        x = np.arange(0, n+1)
        y = [distributions.calculate_binomial_probability(n, i, p) for i in x]
        fig.add_trace(go.Bar(x=x, y=y, name="PMF"))
        
    elif dist_type == "Poisson":
        c1, c2 = st.columns(2)
        rate = c1.number_input("Rate (λ)", 0.1, 100.0, 5.0)
        k = c2.number_input("Events (k)", 0, 100, 5)
        
        prob = distributions.calculate_poisson_distribution(rate, k)
        st.metric(f"P(X={k})", f"{prob:.4f}")
        
        x = np.arange(0, int(rate*3)+5)
        y = [distributions.calculate_poisson_distribution(rate, i) for i in x]
        fig.add_trace(go.Bar(x=x, y=y, name="PMF"))

    elif dist_type == "Normal":
        c1, c2 = st.columns(2)
        mu = c1.number_input("Mean (μ)", value=0.0)
        sigma = c2.number_input("Std Dev (σ)", 0.001, 100.0, 1.0)
        c3, c4 = st.columns(2)
        low = c3.number_input("Lower Bound", value=-1.0)
        high = c4.number_input("High Bound", value=1.0)
        
        prob = distributions.calculate_normal_distribution(mu, sigma, low, high)
        st.metric(f"P({low} ≤ X ≤ {high})", f"{prob:.4f}")
        
        x = np.linspace(mu - 4*sigma, mu + 4*sigma, 200)
        y = (1/(sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu) / sigma)**2)
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='PDF'))
        
        # Fill area
        x_fill = np.linspace(low, high, 100)
        y_fill = (1/(sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x_fill - mu) / sigma)**2)
        fig.add_trace(go.Scatter(x=x_fill, y=y_fill, fill='tozeroy', mode='none', fillcolor='rgba(0,100,80,0.5)', name='Prob Area'))

    elif dist_type == "Geometric":
        c1, c2 = st.columns(2)
        p = c1.number_input("Prob Success (p)", 0.01, 1.0, 0.5)
        k = c2.number_input("Trial (k)", 1, 100, 1)
        
        prob = distributions.calculate_geometric_distribution(p, k)
        st.metric(f"P(X={k})", f"{prob:.4f}")
        
        x = np.arange(1, 20)
        y = [distributions.calculate_geometric_distribution(p, i) for i in x]
        fig.add_trace(go.Bar(x=x, y=y, name="PMF"))

    elif dist_type == "Exponential":
        c1, c2, c3 = st.columns(3)
        rate = c1.number_input("Rate (λ)", 0.01, 100.0, 1.0)
        low = c2.number_input("Lower Time", 0.0, 100.0, 0.0)
        high = c3.number_input("Upper Time", 0.0, 100.0, 2.0)
        
        prob = distributions.calculate_exponential_distribution(rate, low, high)
        st.metric(f"P({low} ≤ T ≤ {high})", f"{prob:.4f}")
        
        x = np.linspace(0, max(high, 5/rate), 200)
        y = rate * np.exp(-rate * x)
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='PDF'))
        
        x_fill = np.linspace(low, high, 100)
        y_fill = rate * np.exp(-rate * x_fill)
        fig.add_trace(go.Scatter(x=x_fill, y=y_fill, fill='tozeroy', mode='none', fillcolor='rgba(200,50,50,0.5)', name='Area'))

    st.plotly_chart(fig, use_container_width=True)

def render_simulations_tab():
    st.header("Monte Carlo Simulations")
    sim_type = st.selectbox("Type", ["Dice Rolls", "Coin Flips", "Card Draws"])
    
    if sim_type == "Dice Rolls":
        c1, c2 = st.columns(2)
        n_dice = c1.number_input("Num Dice", 1, 10, 2)
        n_rolls = c2.number_input("Num Rolls", 100, 100000, 1000)
        
        if st.button("Run Simulation"):
            results = simulations.simulate_dice_rolls(n_dice, n_rolls)
            fig = px.histogram(results, nbins=n_dice*6, title=f"Sum of {n_dice} Dice ({n_rolls} rolls)")
            st.plotly_chart(fig, use_container_width=True)
            stats_res = statistics.calculate_descriptive_stats(results)
            st.json(stats_res)

    elif sim_type == "Coin Flips":
        c1, c2 = st.columns(2)
        n_coins = c1.number_input("Num Coins", 1, 100, 10)
        n_flips = c2.number_input("Num Flips", 100, 100000, 1000)
        
        if st.button("Run Simulation"):
            results = simulations.simulate_coin_flips(n_coins, n_flips)
            fig = px.histogram(results, title=f"Heads in {n_coins} Coin Flips ({n_flips} trials)")
            st.plotly_chart(fig, use_container_width=True)
            st.metric("Expected Heads", n_coins * 0.5)
            st.metric("Observed Mean", np.mean(results))

    elif sim_type == "Card Draws":
        n_draws = st.number_input("Num Draws", 100, 10000, 1000)
        if st.button("Run"):
            results = simulations.simulate_card_draws(n_draws)
            fig = px.histogram(results, title="Sum of 5 Card Values")
            st.plotly_chart(fig, use_container_width=True)

def render_statistics_tab():
    st.header("Statistical Analysis")
    
    st.info("Paste data (comma separated) or generate random data.")
    data_input = st.text_area("Data Input", "12, 15, 14, 16, 15, 13, 15, 14, 18, 14")
    
    try:
        data = [float(x.strip()) for x in data_input.split(',')]
        st.write(f"Loaded {len(data)} data points.")
        
        res = statistics.calculate_descriptive_stats(data)
        st.write("### Descriptive Stats")
        st.dataframe(pd.DataFrame([res]).T.rename(columns={0: "Value"}))
        
        st.write("### Hypothesis Testing")
        if st.checkbox("Perform Z-Test"):
            pop_mean = st.number_input("Population Mean", value=14.0)
            pop_std = st.number_input("Population Std Dev", value=2.0)
            z_res = statistics.perform_z_test(data, pop_mean, pop_std)
            st.write(z_res)
            if z_res['P-Value'] < 0.05:
                st.success("Reject Null Hypothesis (Significant)")
            else:
                st.warning("Fail to Reject Null Hypothesis (Not Significant)")

        if st.checkbox("Perform One-Sample T-Test"):
            pop_mean_t = st.number_input("Hypothesized Mean", value=14.0, key="t_mean")
            t_res = statistics.perform_t_test(data, pop_mean_t)
            st.write(t_res)

    except Exception as e:
        st.error(f"Invalid data format: {e}")

def render_scenarios_tab():
    st.header("🛠️ Situational Tools")
    st.markdown("Specialized calculators for real-world scenarios.")
    
    scenario = st.selectbox("Select Scenario", 
        ["Lottery Probability", "Birthday Paradox", "Poker Outs", "Risk of Ruin", "A/B Test Significance"])
        
    st.markdown("---")
    
    if scenario == "Lottery Probability":
        st.subheader("🎱 Lottery Odds Calculator")
        c1, c2 = st.columns(2)
        total_balls = c1.number_input("Total White Balls", 10, 100, 69)
        pick_white = c2.number_input("White Balls to Pick", 1, 10, 5)
        
        bonus_balls = c1.number_input("Total Bonus Balls (e.g. Red)", 0, 50, 26)
        pick_bonus = c2.number_input("Bonus Balls to Pick", 0, 5, 1)
        
        if st.button("Calculate Odds"):
            prob = scenarios.calculate_lottery_probability(total_balls, pick_white, bonus_balls, pick_bonus)
            st.metric("Win Probability", f"{prob:.12f}")
            if prob > 0:
                st.metric("1 in X Chance", f"1 in {int(1/prob):,}")

    elif scenario == "Birthday Paradox":
        st.subheader("🎂 Birthday Paradox")
        n = st.number_input("Number of People", 2, 366, 23)
        prob = scenarios.calculate_birthday_paradox(n)
        
        col1, col2 = st.columns([1,3])
        col1.metric("Probability of Match", f"{prob:.2%}")
        
        # simple plot
        x = np.arange(1, 101)
        y = [scenarios.calculate_birthday_paradox(i) for i in x]
        fig = px.line(x=x, y=y, title="Probability of Shared Birthday vs Group Size")
        fig.add_hline(y=0.5, line_dash="dash", line_color="red", annotation_text="50% Threshold")
        col2.plotly_chart(fig, use_container_width=True)

    elif scenario == "Poker Outs":
        st.subheader("🃏 Poker Outs Calculator")
        outs = st.number_input("Number of Outs", 1, 20, 9, help="Flush draw = 9, Open Straight = 8")
        cards_to_come = st.radio("Street", ["Turn (2 cards left)", "River (1 card left)"])
        
        n_cards = 2 if "Turn" in cards_to_come else 1
        
        prob = scenarios.calculate_poker_outs(outs, n_cards)
        st.metric("Hit Probability", f"{prob:.2%}")
        
        st.info("Approximation based on standard deck (52 cards).")

    elif scenario == "Risk of Ruin":
        st.subheader("📉 Risk of Ruin")
        c1, c2 = st.columns(2)
        win_rate = c1.number_input("Win Rate (0-1)", 0.0, 1.0, 0.55)
        bankroll = c2.number_input("Bankroll (Units)", 1, 1000, 50)
        
        ror = scenarios.calculate_risk_of_ruin(win_rate, 1, 1, bankroll)
        st.metric("Risk of Ruin", f"{ror:.2%}")
        
        if win_rate <= 0.5:
            st.error("With a win rate <= 50%, ruin is mathematically guaranteed eventually.")

    elif scenario == "A/B Test Significance":
        st.subheader("🅰️/🅱️ A/B Test Calculator")
        c1, c2 = st.columns(2)
        vis_a = c1.number_input("Visitors A", 100, 1000000, 1000)
        conv_a = c1.number_input("Conversions A", 0, vis_a, 100)
        
        vis_b = c2.number_input("Visitors B", 100, 1000000, 1000)
        conv_b = c2.number_input("Conversions B", 0, vis_b, 120)
        
        if st.button("Calculate Significance"):
            p_val, conf = scenarios.calculate_ab_test_significance(conv_a, vis_a, conv_b, vis_b)
            st.metric("Confidence", f"{conf:.2%}")
            st.metric("P-Value", f"{p_val:.4f}")
            
            if conf >= 0.95:
                st.success("Statistically Significant (95%+ Confidence)!")
            else:
                st.warning("Not Significant.")

def main():
    st.set_page_config(page_title="Probability Suite", page_icon="🎲", layout="wide")
    load_css()
    
    st.markdown("""
    <div class="header">
        <h1 class="title">🎲 Probability & Statistics Suite</h1>
        <p class="subtitle">Advanced Analytics, Simulations, and Calculations</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🧩 Probability Logic", 
        "📊 Distributions", 
        "🎲 Simulations", 
        "📈 Statistics",
        "🛠️ Situational Tools"
    ])
    
    with tab1: render_probability_tab()
    with tab2: render_distributions_tab()
    with tab3: render_simulations_tab()
    with tab4: render_statistics_tab()
    with tab5: render_scenarios_tab()

if __name__ == "__main__":
    main()