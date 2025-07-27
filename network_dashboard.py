# To run the script: streamlit run network_dashboard.py

import streamlit as st
import pandas as pd
from scapy.all import sniff, IP, TCP, UDP, ICMP
import plotly.express as px
import time

# Global variables
packets_data = []

def packet_callback(packet):
    """
    Callback function to process captured packets.
    Args:
        packet: Captured packet.
    """
    if IP in packet:
        protocol = "TCP" if TCP in packet else "UDP" if UDP in packet else "ICMP" if ICMP in packet else "Other"
        packets_data.append({
            "timestamp": time.time(),
            "source": packet[IP].src,
            "destination": packet[IP].dst,
            "protocol": protocol,
            "size": len(packet)
        })

def start_packet_capture(interface="eth0", count=100):
    """
    Starts packet capture using Scapy.
    Args:
        interface (str): Network interface to capture packets from.
        count (int): Number of packets to capture.
    """
    sniff(iface=interface, prn=packet_callback, count=count)

def create_visualizations(df):
    """
    Creates visualizations for the Streamlit dashboard.
    Args:
        df (pd.DataFrame): DataFrame containing packet data.
    """
    if len(df) > 0:
        # Protocol distribution chart
        protocol_counts = df['protocol'].value_counts()
        fig_protocol = px.pie(
            values=protocol_counts.values,
            names=protocol_counts.index,
            title="Protocol Distribution"
        )
        st.plotly_chart(fig_protocol, use_container_width=True)

        # Packets timeline chart
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
        df_grouped = df.groupby(df['timestamp'].dt.floor('S')).size()
        fig_timeline = px.line(
            x=df_grouped.index,
            y=df_grouped.values,
            title="Packets per Second"
        )
        st.plotly_chart(fig_timeline, use_container_width=True)

        # Top source IPs chart
        top_sources = df['source'].value_counts().head(10)
        fig_sources = px.bar(
            x=top_sources.index,
            y=top_sources.values,
            title="Top Source IP Addresses"
        )
        st.plotly_chart(fig_sources, use_container_width=True)

def main():
    """
    Main function to run the Streamlit dashboard.
    """
    st.set_page_config(page_title="Network Traffic Analysis", layout="wide")
    st.title("Real-Time Network Traffic Analysis Dashboard")

    # Capture packets and create DataFrame
    interface = st.sidebar.text_input("Enter network interface (e.g., eth0):", value="eth0")
    count = st.sidebar.number_input("Number of packets to capture:", min_value=10, max_value=1000, value=100)
    
    if st.sidebar.button("Start Capture"):
        start_packet_capture(interface=interface, count=count)
    
    if len(packets_data) > 0:
        df = pd.DataFrame(packets_data)
        
        # Display metrics
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Packets Captured", len(df))
        with col2:
            duration = time.time() - df['timestamp'].iloc[0]
            st.metric("Capture Duration", f"{duration:.2f}s")
        
        # Create visualizations
        create_visualizations(df)

        # Display recent packets
        st.subheader("Recent Packets")
        st.dataframe(
            df.tail(10)[['timestamp', 'source', 'destination', 'protocol', 'size']],
            use_container_width=True
        )

if __name__ == "__main__":
    main()

    # Network Interface for Home Network: "Wi-Fi"
    # Start the script in PowerShell Terminal with: streamlit run network_dashboard.py
    
