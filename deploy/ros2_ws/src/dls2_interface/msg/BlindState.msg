# header
dls2_interface/DlsHeader header
string robot_name

# data
string[] joints_name
float64[] joints_position
float64[] joints_velocity
float64[] joints_acceleration
float64[] joints_effort
float64[] joints_temperature
bool[] feet_contact
float64[] current_feet_positions
float64[] motors_current
uint32[] motors_status_word
float64 trunk_temperature
