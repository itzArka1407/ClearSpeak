import streamlit as st

from clearspeak import (
    detect_critical_information,
    transform_for_clarity
)

from rime_tts import generate_speech


# ===================================
# PAGE CONFIGURATION
# ===================================

st.set_page_config(
    page_title="ClearSpeak AI",
    page_icon="🎙️",
    layout="wide"
)


# ===================================
# FUTURISTIC DARK UI
# ===================================

st.markdown("""
<style>

    /* Main background */

    .stApp {
        background: linear-gradient(
            135deg,
            #080b14,
            #101827,
            #090d18
        );
        color: white;
    }


    /* Main title */

    .main-title {
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0px;

        background: linear-gradient(
            90deg,
            #00f5ff,
            #7b61ff,
            #ff4fd8
        );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }


    /* Subtitle */

    .subtitle {
        text-align: center;
        color: #aab4c8;
        font-size: 1.15rem;
        margin-bottom: 30px;
    }


    /* Section cards */

    .card {
        background: rgba(20, 27, 45, 0.85);
        border: 1px solid rgba(0, 245, 255, 0.25);

        border-radius: 15px;

        padding: 20px;

        margin-bottom: 20px;

        box-shadow:
            0px 0px 20px
            rgba(0, 245, 255, 0.08);
    }


    /* Section titles */

    .section-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #00f5ff;

        margin-bottom: 15px;
    }


    /* Detection badge */

    .detection-item {

        background: rgba(123, 97, 255, 0.12);

        border-left:
            4px solid #7b61ff;

        padding: 12px;

        border-radius: 8px;

        margin-bottom: 10px;

        color: white;
    }


    /* Text area */

    textarea {

        background-color: #111827 !important;

        color: white !important;

        border:
            1px solid #00f5ff !important;

        border-radius: 10px !important;
    }


    /* Buttons */

    .stButton button {

        width: 100%;

        border-radius: 10px;

        font-size: 1.05rem;

        font-weight: 700;

        padding: 12px;

        border: none;

        background:
            linear-gradient(
                90deg,
                #00c6ff,
                #7b61ff
            );

        color: white;

        transition: 0.3s;
    }


    .stButton button:hover {

        transform: scale(1.02);

        box-shadow:
            0px 0px 20px
            rgba(0, 245, 255, 0.5);
    }


    /* Download button */

    .stDownloadButton button {

        width: 100%;

        border-radius: 10px;

        font-weight: 600;
    }


    /* Divider */

    hr {

        border-color:
            rgba(0, 245, 255, 0.2);
    }


</style>
""", unsafe_allow_html=True)


# ===================================
# HERO SECTION
# ===================================

st.markdown(
    """
    <div class="main-title">
        🎙️ ClearSpeak AI
    </div>

    <div class="subtitle">
        Intelligent Critical Information Detection
        •
        Speech Optimization
        •
        AI Voice Delivery
    </div>
    """,

    unsafe_allow_html=True
)


st.divider()


# ===================================
# INPUT SECTION
# ===================================

st.markdown(
    """
    <div class="card">

    <div class="section-title">
        📝 Input Message
    </div>

    Enter any message containing important
    information such as OTPs, phone numbers,
    times, payment amounts or reference IDs.

    </div>
    """,

    unsafe_allow_html=True
)


user_text = st.text_area(

    "Enter your message",

    placeholder=(
        "Example: Your OTP is 583291. "
        "Call 9876543210 at 4:30 PM. "
        "Your payment amount is ₹1,500."
    ),

    height=160,

    label_visibility="collapsed"
)


# ===================================
# PROCESSING
# ===================================

if user_text.strip():

    st.divider()


    # ===================================
    # TWO COLUMN LAYOUT
    # ===================================

    left_column, right_column = st.columns(2)


    # ===================================
    # LEFT COLUMN
    # ORIGINAL MESSAGE
    # ===================================

    with left_column:

        st.markdown(
            """
            <div class="card">

            <div class="section-title">
                📄 Original Message
            </div>

            </div>
            """,

            unsafe_allow_html=True
        )

        st.info(user_text)


        # ===================================
        # DETECTION
        # ===================================

        detected_info = (
            detect_critical_information(
                user_text
            )
        )


        st.markdown(
            """
            <div class="section-title">
                🔍 Critical Information
            </div>
            """,

            unsafe_allow_html=True
        )


        if detected_info:

            for item in detected_info:

                st.markdown(

                    f"""
                    <div class="detection-item">

                    <b>{item['type']}</b>

                    <br>

                    {item['value']}

                    </div>
                    """,

                    unsafe_allow_html=True
                )

        else:

            st.warning(
                "No critical information detected."
            )


    # ===================================
    # RIGHT COLUMN
    # CLEARSPEAK OUTPUT
    # ===================================

    with right_column:

        transformed_text = (
            transform_for_clarity(
                user_text
            )
        )


        st.markdown(
            """
            <div class="card">

            <div class="section-title">
                🧠 ClearSpeak AI Processing
            </div>

            Critical information has been
            transformed for clearer speech
            delivery.

            </div>
            """,

            unsafe_allow_html=True
        )


        st.markdown(
            """
            <div class="section-title">
                🗣️ Speech-Optimized Message
            </div>
            """,

            unsafe_allow_html=True
        )


        st.success(
            transformed_text
        )


    # ===================================
    # AUDIO SECTION
    # ===================================

    st.divider()


    st.markdown(
        """
        <div class="card">

        <div class="section-title">
            🎙️ AI Voice Generation
        </div>

        Generate natural speech using the
        ClearSpeak optimized message.

        </div>
        """,

        unsafe_allow_html=True
    )


    # ===================================
    # AUDIO BUTTON
    # ===================================

    if st.button(
        "🔊 GENERATE CLEARSPEAK AUDIO"
    ):

        try:

            with st.spinner(
                "🧠 ClearSpeak is generating AI voice..."
            ):

                audio_data = generate_speech(
                    transformed_text
                )


            st.success(
                "🎉 AI voice generated successfully!"
            )


            # AUDIO PLAYER

            st.audio(
                audio_data,
                format="audio/mp3"
            )


            # DOWNLOAD

            st.download_button(

                label="⬇️ DOWNLOAD AUDIO",

                data=audio_data,

                file_name="clearspeak_audio.mp3",

                mime="audio/mpeg"
            )


        except Exception as error:

            st.error(
                f"Audio generation failed: {error}"
            )


# ===================================
# EMPTY STATE
# ===================================

else:

    st.markdown(
        """
        <div class="card">

        <div class="section-title">
            🚀 Ready to Begin
        </div>

        Enter a message above and ClearSpeak AI
        will automatically detect and optimize
        critical information for voice delivery.

        </div>
        """,

        unsafe_allow_html=True
    )


# ===================================
# FOOTER
# ===================================

st.divider()

st.markdown(

    """
    <div style="text-align:center;
                color:#6f7a91;
                padding:20px;">

        ClearSpeak AI • Intelligent Voice Clarity

    </div>
    """,

    unsafe_allow_html=True
)