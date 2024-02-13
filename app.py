
import numpy as np
from bearing import Bearing
from coupling import Coupling
from fan import Fan
from gearbox import Gearbox
import streamlit as st
import time
from streamlit_autorefresh import st_autorefresh
import util
import plotly.graph_objects as go

class Machine:
    def __init__(self):
        self.equipments = []

    def connect(self, equipment):
        self.equipments.append(equipment)
        if len(self.equipments) > 1:
            self.equipments[0].connect(self.equipments[1])
        return self
    def drive(self, rpm, duration):
        head=self.equipments[0]
        if head is not None:
            return head.drive(rpm, duration)
        else:
            return None



#defining states
if 'machine' not in st.session_state:
    st.session_state.machine = Machine()
if 'editing_equipment' not in st.session_state:
    st.session_state.editing_equipment = None
if 'autoplay' not in st.session_state:
    st.session_state.autoplay = True
if 'rpm' not in st.session_state:
    st.session_state.rpm = 2000


#initializing session state variables
machine = st.session_state.machine
editing_equipment = st.session_state.editing_equipment
autoplay = st.session_state.autoplay

#initializing callbacks
def stop_autoplay():
    st.session_state.autoplay = False

def start_autoplay():
    st.session_state.autoplay = True

def delete_equipment(eq):
    st.session_state.autoplay = False
    if eq == editing_equipment:
        st.session_state.editing_equipment = None
    if eq in machine.equipments:
        machine.equipments.remove(eq)
    st.session_state.editing_equipment = None

def edit_equipment(eq):
    st.session_state.autoplay = False
    st.session_state.editing_equipment = eq
def set_rpm(rpm):
    st.session_state.rpm = rpm
# Container for page content
content = st.container()

# Clear previous content
content.empty()

st.title("Faultsim")
st.text("By Sensemore Team")

rpm =st.sidebar.slider("RPM", 100, 100000, st.session_state.rpm, key="rpm")

add_random_noise = st.sidebar.checkbox("Random Noise", key="random_noise", value=st.session_state.get("random_noise", False))
add_harmonic_interference = st.sidebar.checkbox("Harmonic Interference", key="harmonic_interference", value=st.session_state.get("harmonic_interference", False))
add_transient_spikes = st.sidebar.checkbox("Transient Spikes", key="transient_spikes", value=st.session_state.get("transient_spikes", False))

if autoplay:
    st.sidebar.button("Stop Autoplay", key="stop_autoplay", on_click=stop_autoplay)
else :
    st.sidebar.button("Start Autoplay", key="start_autoplay", on_click=start_autoplay)


if editing_equipment is None:
# Sidebar for adding equipment
    st.sidebar.title("Add Equipment")
    equipment_type = st.sidebar.selectbox("Select Equipment Type", ( "Bearing", "Coupling", "Fan", "Gearbox"))

    # Default properties based on equipment type
    if equipment_type == "Bearing":
        defect_type = st.sidebar.selectbox("Defect Type", ("inner_race", "outer_race", "ball", "cage"))
        BPFI = st.sidebar.number_input("BPFI", value=100)
        BPFO = st.sidebar.number_input("BPFO", value=90)
        BSF = st.sidebar.number_input("BSF", value=50)
        FTF = st.sidebar.number_input("FTF", value=10)
        if st.sidebar.button("Add Bearing"):
            machine.connect(Bearing({'BPFI': BPFI, 'BPFO': BPFO, 'BSF': BSF, 'FTF': FTF,'defect_type':defect_type}))
    elif equipment_type == "Coupling":
        misalignment= st.sidebar.number_input("Misalignment", value=0.2)
        wear= st.sidebar.number_input("Wear", value=0.1)
        if st.sidebar.button("Add Coupling"):
            machine.connect(Coupling({'misalignment': misalignment, 'wear': wear}))
    elif equipment_type == "Fan":
        blade_frequency = st.sidebar.number_input("Blade Frequency", value=100)
        imbalance = st.sidebar.number_input("Imbalance", value=0.2)
        if st.sidebar.button("Add Fan"):
            machine.connect(Fan({'Blade Pass Frequency': blade_frequency, 'Imbalance': imbalance}))
    elif equipment_type == "Gearbox":
        gearmesh_frequency = st.sidebar.number_input("Gearmesh Frequency", value=100)
        misalignment= st.sidebar.number_input("Misalignment", value=0.2)
        wear= st.sidebar.number_input("Wear", value=0.1)
        if st.sidebar.button("Add Gearbox"):
            machine.connect(Gearbox({'Gear Mesh Frequency': gearmesh_frequency, 'Misalignment': misalignment, 'Wear': wear}))
else:
    st.sidebar.button("Add Equipment", key="add_equipment", on_click=edit_equipment, args=(None,))
    st.sidebar.title(f"Editing: {editing_equipment.name} ({editing_equipment.type})")
    st.sidebar.text("Edit Equipment")

    if editing_equipment.type=="bearing":
        

        defect_type = st.sidebar.selectbox("Defect Type", ("inner_race", "outer_race", "ball", "cage"))
        BPFI = st.sidebar.number_input("BPFI", value=editing_equipment.properties.get('BPFI', 100)) 
        BPFO = st.sidebar.number_input("BPFO", value=editing_equipment.properties.get('BPFO', 90))
        BSF = st.sidebar.number_input("BSF", value=editing_equipment.properties.get('BSF', 50))
        FTF = st.sidebar.number_input("FTF", value=editing_equipment.properties.get('FTF', 10))
                          
        editing_equipment.properties['defect_type']= defect_type
        editing_equipment.properties['BPFI'] = BPFI
        editing_equipment.properties['BPFO'] = BPFO
        editing_equipment.properties['BSF'] = BSF
        editing_equipment.properties['FTF'] = FTF

    elif editing_equipment.type=="fan":
        blade_frequency = st.sidebar.number_input("Blade Frequency", value=editing_equipment.properties.get('Blade Pass Frequency', 100))
        imbalance = st.sidebar.number_input("Imbalance", value=editing_equipment.properties.get('Imbalance', 0.2))
        editing_equipment.properties['Blade Pass Frequency'] = blade_frequency
        editing_equipment.properties['Imbalance'] = imbalance

    elif editing_equipment.type=="coupling":
        misalignment = st.sidebar.number_input("Misalignment", value=editing_equipment.properties.get('misalignment', 0.2))
        wear = st.sidebar.number_input("Wear", value=editing_equipment.properties.get('wear', 0.1))
        editing_equipment.properties['misalignment'] = misalignment
        editing_equipment.properties['wear'] = wear

    elif editing_equipment.type=="gearbox":
        gearmesh_frequency = st.sidebar.number_input("Gearmesh Frequency", value=editing_equipment.properties.get('Gear Mesh Frequency', 100))
        misalignment = st.sidebar.number_input("Misalignment", value=editing_equipment.properties.get('Misalignment', 0.2))
        wear = st.sidebar.number_input("Wear", value=editing_equipment.properties.get('Wear', 0.1))
        editing_equipment.properties['Gear Mesh Frequency'] = gearmesh_frequency
        editing_equipment.properties['Misalignment'] = misalignment
        editing_equipment.properties['Wear'] = wear

    
    st.sidebar.button("Delete", on_click=delete_equipment, args=(editing_equipment,))


#render equipment buttons
st.write("Connected Equipments:")
if len(machine.equipments) != 0:
    cols = st.columns(len(machine.equipments))
    for i, eq in enumerate(machine.equipments):
        with cols[i]:
            st.button(f"{eq.type}({eq.name})", key=eq.name, on_click=edit_equipment, args=(eq,))

chart1_placeholder = st.empty()
chart2_placeholder = st.empty()

#render charts
if len(machine.equipments) != 0:
    while True:
        t, signal = machine.drive(rpm=rpm, duration=1)
        sampling_rate = 1000
        if add_random_noise:
            signal = util.add_random_noise(signal)
        if add_harmonic_interference:
            signal = util.add_harmonic_interference(signal, t, interference_freqs=[50, 150], amplitudes=[0.05, 0.02], phases=[0, np.pi/4])
        if add_transient_spikes:
            signal = util.add_transient_spikes(signal, t, spike_times=[0.5, 1, 1.5], spike_amplitude=0.1, spike_duration=0.1)

        fft = np.abs(np.fft.fft(signal))[0:len(signal)//2]
        f=np.fft.fftfreq(len(signal), d=1/sampling_rate)[0:len(signal)//2]  
        #update trace data

        chart2_placeholder.plotly_chart(go.Figure(data=[go.Scatter(x=f, y=fft)],layout=go.Layout(title="Spectrum",height=300)), use_container_width=True)
        chart1_placeholder.plotly_chart(go.Figure(data=[go.Scatter(x=t, y=signal)], layout=go.Layout(title="Signal",height=300)), use_container_width=True)
        if not autoplay:
            break;
        time.sleep(0.4)

else:

    #init two plot with height 300px
    signal_trace=go.Scatter(x=[], y=[])
    spectrum_trace=go.Scatter(x=[], y=[])

    signal_fig=go.Figure(data=[signal_trace])
    spectrum_fig=go.Figure(data=[spectrum_trace])

    signal=st.plotly_chart(signal_fig, use_container_width=True)
    spectrum=st.plotly_chart(spectrum_fig, use_container_width=True)