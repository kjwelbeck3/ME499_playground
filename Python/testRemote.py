from labview_automation import LabVIEW
lv = LabVIEW(host="10.42.0.100")
lv.start()  # Launches the active LabVIEW with the listener VI

with lv.client() as c:
    vi_path = r'C:\Users\Ping Guo\Documents\onedrive_backup\OneDrive - Northwestern University\Desktop\KojoWelbeck\ProjectEnvironment\Python\playground\AddTwo.vi'
    control_values = {
    "Numeric": 1,
    "Numeric 2": 9876
}
indicators = c.run_vi_synchronous(
    vi_path, control_values, indicator_names=["Numeric 3"])
print(indicators['Numeric'])
# error_message = c.describe_error(indicators['Error Out'])
lv.kill()  # Stop LabVIEW
