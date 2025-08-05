import time
import streamlit as st

# --- Custom CSS for headers ---
# The !important flag is used to ensure these styles override Streamlit's defaults.
st.markdown("""
<style>
    /* Target h2 elements (st.header) and force light yellow color */
    h2 {
        color: #ffe576 !important; /* light yellow */
    }
            
    /* Target the text of h3 elements (st.subheader) and force light yellow color */
    h3 {
        color: #ffe576 !important; /* light yellow */
    }

    /* Target links *within* h3 (st.subheader) */
    h3 a:link, h3 a:visited {
        color: #bcd9ff; /* periwinkle */
        text-decoration: none; /* Optional: remove underline */
    }

    /* Optional: Change color on hover for links within h3 */
    h3 a:hover {
        color: #bcfffe; /* light blue */
        text-decoration: underline; /* Optional: add underline on hover */
    }

    /* General links outside of h3, if any, or to define a default */
    a:link, a:visited {
        color: #007bff; /* Standard blue for other links */
    }
    a:hover {
        color: #0056b3;
    }
</style>
""", unsafe_allow_html=True)

# --- Stopwatch Logic and Session State Initialization (Moved out of main for clarity) ---
# Initialize Session State for Stopwatch
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'elapsed_time' not in st.session_state:
    st.session_state.elapsed_time = 0.0
if 'running' not in st.session_state:
    st.session_state.running = False
if 'stop_offset' not in st.session_state: # To handle pauses
    st.session_state.stop_offset = 0.0

def start_stopwatch():
    if not st.session_state.running:
        st.session_state.start_time = time.time() - st.session_state.stop_offset
        st.session_state.running = True

def stop_stopwatch():
    if st.session_state.running:
        st.session_state.stop_offset = time.time() - st.session_state.start_time
        st.session_state.running = False

def reset_stopwatch():
    st.session_state.start_time = None
    st.session_state.elapsed_time = 0.0
    st.session_state.running = False
    st.session_state.stop_offset = 0.0

def balloons():
    st.balloons()

# --- Main Application Function ---
def main():
    st.set_page_config(layout="wide") 
    st.title("Streamlit Resources and Demos")

    # ===== Sidebar =====
    with st.sidebar:
        # --- User Input ---
        name = st.text_input("What is your name?", placeholder="type your name here",)
        if name:
            st.title(f"*Welcome {name}!*")

        st.markdown('##')
        # --- Timer ---
        st.title("Time how long you explore!")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.button("Start", on_click=start_stopwatch)
        with col2:
            st.button("Stop", on_click=stop_stopwatch)
        with col3:
            st.button("Reset", on_click=reset_stopwatch)

        time_placeholder = st.empty() # placeholder for timer

        # - Live Stopwatch Display Logic -
        if st.session_state.running:
            # Loop while the stopwatch is running to update the display smoothly
            while st.session_state.running:
                current_elapsed_time = time.time() - st.session_state.start_time
                minutes, seconds = divmod(current_elapsed_time, 60)
                hours, minutes = divmod(minutes, 60)
                formatted_time = f"{int(hours):02}:{int(minutes):02}:{seconds:05.2f}"

                # Update the content of the placeholder
                time_placeholder.markdown(f"## {formatted_time}", unsafe_allow_html=False)

                # Wait a small amount of time to control update frequency
                time.sleep(0.05) # Update roughly 20 times per second

                # Important: Do NOT use st.rerun() inside this while loop
                # because it would cause infinite reruns that block the UI.
                # The while loop with st.empty() and time.sleep() handles live updates.
        else:
            # When not running, just display the final elapsed time or 0.0
            minutes, seconds = divmod(st.session_state.elapsed_time, 60)
            hours, minutes = divmod(minutes, 60)
            formatted_time = f"{int(hours):02}:{int(minutes):02}:{seconds:05.2f}"
            time_placeholder.markdown(f"## {formatted_time}", unsafe_allow_html=False)

        # --- Balloons ---
        st.markdown('##')
        st.title("Looking for fun?")
        st.button("Click for a surprise!", on_click=balloons)

    # ===== Tabs ======
    # The sections you want to be clickable as tabs at the top of the main content area
    tab_resources, tab_live_assessment, tab_visuals, tab_demos = st.tabs([
        "Resources", 
        "Live Assessment Tools", 
        "Visuals", 
        "Fun Demos"
    ])
            
    # Content for the "Resources" tab
    with tab_resources:
        st.header("⭐ Don’t know where to start?")
        st.write("Here are some great resources to get you started with Streamlit:")

        st.subheader("[1. Streamlit: The Fastest Way To Build Python Apps?](https://youtu.be/D0D4Pa22iG0?si=tUxEDzE7N9IsxRD8)")
        st.write("Watch up to 3:22 to learn how to set up Streamlit and take input in your app.")
        col1, col2 = st.columns(2)
        with col1:
            st.video("https://youtu.be/D0D4Pa22iG0?si=tUxEDzE7N9IsxRD8", width=500)
        with col2: 
            st.write("Optional: watch the rest of the video to learn about:")
            st.markdown("""
            * 00:00 Introduction
            * 00:41 What is Streamlit?
            * 01:49 Using Input Elements
            * 03:22 Working with Data
            * 04:47 Multipage Apps
            * 06:43 Loan Repayments App
            * 10:03 Deploying to Streamlit Cloud
            """)

        st.subheader("[2. Building a dashboard in Python using Streamlit](https://blog.streamlit.io/crafting-a-dashboard-app-in-python-using-streamlit/)")
        st.write("A great resource for understanding the format and simple capabilities of Streamlit applications.")
        st.markdown("""
        * Breaks down the formatting
        * Guides you through the code → follow along to experiment on your own
        """)

        st.subheader("[3. Streamlit API Reference](https://docs.streamlit.io/develop/api-reference)")
        st.write("Check out the code of Streamlit elements.")

        st.subheader("[4. GitHub - Learn how to build Streamlit application in Data Science](https://github.com/laxmimerit/streamlit-tutorials)")
        st.write("Github Tutorial for going through Streamlit functions.")

        st.subheader("5. [Streamlit-extras](https://extras.streamlit.app/?ref=streamlit-io-gallery-favorites)")
        st.write("A library that allows you to simplify code/functions with emojis.")
        st.markdown("---") 

    # Content for the "Live Assessment Tools" tab
    with tab_live_assessment:
        st.header("💻 Live Assessment Related Tutorials")

        col3, col4 = st.columns(2)
        with col3:
            st.subheader("Tutorials")
            st.markdown("---") # Separator

            st.subheader("[How to Work with Databases in Streamlit](https://docs.streamlit.io/develop/tutorials/databases)")
            st.write("Great for understanding how to connect to databases.")

            st.subheader("[How to Transcribe Audio to Text with AI and Streamlit](https://www.youtube.com/watch?v=JJEXqi85fOk)")
            st.write("Audio Transcription App")

            st.subheader("[Step-by-Step Guide to Building an AI Voice Assistant with Streamlit & OpenAI 1HR](https://www.youtube.com/watch?v=ZLiA_pkRFsc)")
            st.write("Creating a Voice Assistant using Streamlit.")
            st.warning("Issue: Uses Whisper API (costly)")

        with col4:
            st.subheader("Chatbot Demos")
            st.markdown("---")
            
            st.write("[**GPT Lab**](https://gptlab.streamlit.app/?ref=streamlit-io-gallery-trending)")
            st.write("Speak to pre-trained AI Assistants with different personalities and purposes, or create your own.")
            st.info("Requires OpenAI API Key, but still check out the website because it looks really clean.")
            
            st.write("[**snowChat**](https://snowchat.streamlit.app/?ref=streamlit-io-gallery-llms)")
            st.write("Generates SQL-code. No chat memory, I believe. Does not require API key.")
            
            st.write("[**🦙💬 Llama 2 Chatbot**](https://llama2.streamlit.app/?ref=streamlit-io-gallery-trending)")
            st.write("Runs, but was incredibly slow when I tested it.")
            st.write("Created for the user to change the temp, top_p, and max length parameters of the models.")
        st.markdown("---") 

    # Content for the "Visuals" tab
    with tab_visuals:
        st.header("💐 Visuals")

        st.subheader("[Anthropic Theming Example of Streamlit Elements](https://doc-theming-overview-anthropic-light-inspired.streamlit.app/)")
        st.write("Highly recommend looking at this to see what you can incorporate into your projects.")

        st.subheader("[Make your Streamlit App Look Better | by Yash Chauhan | Accredian | Medium](https://medium.com/accredian/make-your-streamlit-web-app-look-better-14355c2db871)")
        st.write("How to improve UI of your Streamlit Project.")

        st.subheader("[Streamlit Design System | Figma](https://www.figma.com/community/file/1166786573904778097)")
        st.write("Use this Figma Page to help you design your app.")

        st.subheader("[Streamlit emoji shortcodes](https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/)")
        st.write("How to implement emojis in your app. But I have been able to just type emojis directly.")

        st.write("[**Streamlit Elements**](https://github.com/okld/streamlit-elements)")
        st.write("Cool drag and drop components for Streamlit.")

        st.markdown("---")

    # Content for the "Fun Demos" tab
    with tab_demos:
        st.header("🚀 Explore Demos (Ranked from most to least interesting according to Christina):")

        st.subheader("[**Super Awesome Streamlit Apps & Components 🎈**](https://shru.hashnode.dev/super-awesome-streamlit-apps-components)")
        st.write("Simple Demos that I found interesting: fruit classification projects, video players, and LinkedIn Connection Insight apps.")

        st.subheader("[**Goodreads Analysis App**](https://goodreads.streamlit.app/)")
        st.write("Good display of functions you can incorporate into a Streamlit Project.")

        st.subheader("[**PixMatch**](https://pixmatchgame.streamlit.app/?ref=streamlit-io-gallery-favorites)")
        st.write("Matching Game!")

        st.subheader("[Streamlit Favorites Gallery](https://streamlit.io/gallery?category=favorites)")
        st.write("Streamlit’s Listing of Top Projects.")

        st.subheader("[Streamlit Folium](https://folium.streamlit.app/)")
        st.write("If you like looking at maps.")

        st.subheader("[Replicate Image Generator](https://generateimages.streamlit.app/?ref=streamlit-io-gallery-favorites)")
        st.info("Cool, but requires API key.")

        st.markdown("---") 

        st.markdown("**TIP:** Like a Demo you see? Fork the code on GitHub (Check top right of website and sometimes the GitHub is included) and change it to be your own!")

# --- Run the main application ---
if __name__ == "__main__":
    main()