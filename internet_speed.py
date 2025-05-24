import streamlit as st
import speedtest
import plotly.graph_objects as go

# Function to get internet speed
def get_internet_speed():
    st = speedtest.Speedtest()

    try:
        # Get best server
        st.get_best_server()

        # Get download, upload speed, and ping
        download_speed = st.download() / 1_000_000  # Convert from bps to Mbps
        upload_speed = st.upload() / 1_000_000  # Convert from bps to Mbps
        ping = st.results.ping

        return download_speed, upload_speed, ping
    except Exception as e:
        st.error(f"Error while testing the internet speed: {e}")
        return None, None, None

# Function to create and display a gauge
def create_gauge(value, title, color, range_max=100):
    return go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': title},
        gauge={
            'axis': {'range': [0, range_max]},
            'bar': {'color': color}
        }
    ))

# Streamlit App
def app():
    st.title('Internet Speed Test')
    st.write('Check your internet speed with live testing.')

    # Add a button to trigger the speed test
    if st.button('Run Speed Test'):
        with st.spinner('Running the speed test...'):
            # Run the speed test
            download_speed, upload_speed, ping = get_internet_speed()

            if download_speed is not None and upload_speed is not None and ping is not None:
                # Display results
                st.subheader(f"Download Speed: {download_speed:.2f} Mbps")
                st.subheader(f"Upload Speed: {upload_speed:.2f} Mbps")
                st.subheader(f"Ping: {ping} ms")

                # Display gauges for download, upload, and ping
                st.plotly_chart(create_gauge(download_speed, "Download Speed (Mbps)", "blue"))
                st.plotly_chart(create_gauge(upload_speed, "Upload Speed (Mbps)", "green"))
                st.plotly_chart(create_gauge(ping, "Ping (ms)", "red", range_max=200))  # Adjust ping range for better visualization
            else:
                st.warning("Unable to perform the speed test. Please try again later.")

if __name__ == "__main__":
    app()
