
import os
import subprocess
from env.custom_pymavlink import Custom_mav  
import psutil


class Sitl():

    def __init__(self,args) -> None:
        self.container_ip = args["container_ip"] # "172.17.0.2"
        self.mission_planner_ip = args["mp_host_ip"] # "10.0.0.33"
        self.mav_outport = args["mav_outport"] # 14551 
        self.mission_planner_port = args["mp_port"] # 14550
        self.SIM_RATE_HZ = args["SIM_RATE_HZ"]
        self.SIM_GPS_HZ = args["SIM_GPS_HZ"]
        self.sitl = None
        self.myMav = Custom_mav(ip_sitl=self.container_ip,port=self.mav_outport)


    def run(self) -> None:
        self.progress("run ArduCopter")
        autotest_folder = "/ardupilot/Tools/autotest"
        os.chdir(path=autotest_folder)
        try:
            if self.mission_planner_ip is not None:
                self.sitl = subprocess.Popen(["sim_vehicle.py","-v","ArduCopter","--out",f"{self.container_ip}:{self.mav_outport}","--out",f"{self.mission_planner_ip}:{self.mission_planner_port}"],stdout=subprocess.PIPE, stderr=subprocess.PIPE,stdin=subprocess.PIPE, text=True)
            else: 
                self.sitl = subprocess.Popen(["sim_vehicle.py","-v","ArduCopter","--out",f"{self.container_ip}:{self.mav_outport}"],stdout=subprocess.PIPE, stderr=subprocess.PIPE,stdin=subprocess.PIPE, text=True)
        except subprocess.CalledProcessError as e:
            print(f"command failed with return code:{e.returncode}")

        while True:   
            new_line = self.sitl.stdout.readline()
            self.progress(new_line)

            if "Flight" in new_line:
                self.progress("call to pymavlink")
                self.myMav.connect()
                break

        self.write_to_process(command=f"param set SIM_RATE_HZ {self.SIM_RATE_HZ}\n")
        self.write_to_process(command=f"param set SIM_GPS_HZ {self.SIM_GPS_HZ}\n")
        self.write_to_process(command="mode GUIDED\n")

        self.myMav.arm_copter()

        self.myMav.takeoff_to10m()

        self.write_to_process(command="mode STABILIZE\n")

        return 0


    def set_rc(self,rc_channels) -> None:
        self.myMav.send_rc_command(rc_channel_values=rc_channels)

    def get_gps_and_attitude(self) -> None:
        gps = self.myMav.get_gps()
        attitude = self.myMav.get_attitude()
        return gps , attitude
            
    def write_to_process(self,command) -> None:
        self.sitl.stdin.write(command)
        self.sitl.stdin.flush()

    def close(self) -> None:
        self.myMav.close()
        self.write_to_process(command=f"output remove {self.mission_planner_ip}:{self.mission_planner_port} {self.container_ip}:{self.mav_outport} \n")
        self.kill_all_process()

    def kill_all_process(self) -> None:
        parent = psutil.Process(self.sitl.pid)
        for child in parent.children(recursive=True):
            child.terminate()
        parent.terminate()
        remaining_processes = ["run_in_terminal","arducopter"]
        for process_name in remaining_processes:
            self.kill_process_by_name(process_name)

    def kill_process_by_name(self,process_name) -> None:
        for process in psutil.process_iter(['pid', 'name']):
            if process.info['name'] == process_name:
                try:
                    process_obj = psutil.Process(process.info['pid'])
                    process_obj.terminate()
                except Exception as e:
                    print(f"Error terminating process {process_name}: {e}")

    def progress(self,arg) -> None:
        print(f"SITL: {arg}\n")

