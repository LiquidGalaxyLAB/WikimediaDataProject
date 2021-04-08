import os
import netifaces as ni
import time

from .kml_generator import *

file_kmls_txt_path = "kml_tmp/kmls.txt"
file_query_txt_path = "kml_tmp/query.txt"
serverPath = "/var/www/html/"
serverPath_query = "/tmp/"

class Project_configuration(object):

    def __init__(self):
        print("Project configuration ...")

    def get_galaxy_ip(self):
        f = open(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + '/galaxy_ip', 'r')
        ip_galaxy_master = f.read()
        f.close()
        return ip_galaxy_master

    def get_server_ip(self):
        ni.ifaddresses('wlp3s0')
        ip_server = ni.ifaddresses('wlp3s0')[2][0]['addr']
        return ip_server

    def sendKML_ToGalaxy(self, kml_file, kml_name):
    	ip_galaxy_master = self.get_galaxy_ip()
    	ip_server = self.get_server_ip()

    	file = open("kml_tmp/kmls.txt", 'w+')
    	file.write("http://" + str(ip_server) + ":8000/static/kml/" + str(kml_name)+".kml?a=" + str(int(round(time.time()))) + "\n")
    	file.close()

    	os.system("sshpass -p 'lqgalaxy' scp " + file_kmls_txt_path + " lg@"+ ip_galaxy_master +":" + serverPath)

    	print ("KML send!!")

    def write_FlyTo_andSend(self, kml_file_name):
    	ip_galaxy_master = self.get_galaxy_ip()
    	ip_server = self.get_server_ip()

    	file = open(kml_file_name, 'r+')
    	line = file.read()
    	flyto_text = line.split("<LookAt>")[1].split("</LookAt")[0]
    	file.close()

    	file = open("kml_tmp/query.txt", 'w+')
    	file.write("flytoview=<LookAt>"+flyto_text+"</LookAt>" + '\n')
    	file.close()

    	os.system("sshpass -p 'lqgalaxy' scp " + file_query_txt_path + " lg@"+ ip_galaxy_master +":" + serverPath_query)

    def flyTo_initialize(self):
    	ip_galaxy_master = self.get_galaxy_ip()
    	ip_server = self.get_server_ip()

    	flyto_text = "<LookAt><longitude>-5.440476536074238</longitude><latitude>40.58746164894497</latitude><altitude>0</altitude><heading>-2.736639243772986</heading><tilt>0</tilt><range>17068458.20986722</range><altitudeMode>relativeToSeaFloor</altitudeMode></LookAt>"

    	file = open("kml_tmp/query.txt", 'w+')
    	file.write("flytoview="+ flyto_text + '\n')
    	file.close()

    	os.system("sshpass -p 'lqgalaxy' scp " + file_query_txt_path + " lg@"+ ip_galaxy_master +":" + serverPath_query)

    def flyTo_nearStadiums(self):
        ip_galaxy_master = self.get_galaxy_ip()
        ip_server = self.get_server_ip()

        flyto_text = "<LookAt><longitude>-2.847224</longitude><latitude>52.894877</latitude><altitude>0</altitude><heading>-2.736639243772986</heading><tilt>0</tilt><range>2500000</range><altitudeMode>relativeToGround</altitudeMode></LookAt>"

        file = open("kml_tmp/query.txt", 'w+')
        file.write("flytoview="+ flyto_text + '\n')
        file.close()

        os.system("sshpass -p 'lqgalaxy' scp " + file_query_txt_path + " lg@"+ ip_galaxy_master +":" + serverPath_query)

    def sendEarthOrbitFile_ToGalaxy(self,case):
    	ip_galaxy_master = self.get_galaxy_ip()
    	ip_server = self.get_server_ip()

    	if case == "cities":
    	    kml_text = ":8000/static/utils/earth_rotation_zoom.kml\n"
    	else:
    	    kml_text = ":8000/static/utils/earth_rotation.kml\n"

    	with open("kml_tmp/kmls.txt", 'a') as file:
    	    file.write("http://" + str(ip_server) + kml_text)
    	file.close()

    	os.system("sshpass -p 'lqgalaxy' scp " + file_kmls_txt_path + " lg@"+ ip_galaxy_master +":" + serverPath)
    	time.sleep(2)
    	file = open("kml_tmp/query.txt", 'w+')
    	file.write("playtour=EarthOrbit")
    	file.close()

    	os.system("sshpass -p 'lqgalaxy' scp " + file_query_txt_path + " lg@"+ ip_galaxy_master +":" + serverPath_query)
    	print("Query.txt send!!")

    def start_tour_premier_league(self):
    	ip_galaxy_master = self.get_galaxy_ip()
    	ip_server = self.get_server_ip()

    	file = open("kml_tmp/query.txt", 'w+')
    	file.write("playtour=Stadium Tour")
    	file.close()

    	os.system("sshpass -p 'lqgalaxy' scp " + file_query_txt_path + " lg@"+ ip_galaxy_master +":" + serverPath_query)

    def generate_kml(self, use_case, data_set, icon, kml_name):
    	print("Generating KML file ...", icon)
    	generator_kml = GeneratorKML(data_set, kml_name ,"")

    	if use_case == "Tour Cities":
    		kml_file = generator_kml.generateKML_Tour_Cities()
    		self.flyTo_initialize()
    		self.sendKML_ToGalaxy(kml_file, kml_name)
    		self.sendEarthOrbitFile_ToGalaxy("cities")

    	elif use_case == "Premier League Stadiums":
    		kml_file = generator_kml.generateKML_premierLeague_Stadiums(icon)
    		self.write_FlyTo_andSend(kml_file.name)
    		self.sendKML_ToGalaxy(kml_file, kml_name)
    		time.sleep(10)
    		self.start_tour_premier_league()

    	elif use_case == "Tour Premier League Stadiums":
    		kml_file = generator_kml.generateKML_Tour_PremierLeague_Stadiums()
    		self.flyTo_initialize()
    		self.flyTo_nearStadiums()
    		self.sendKML_ToGalaxy(kml_file, kml_name)

    	elif use_case == "Longest Rivers":
    		kml_file = generator_kml.generateKML_Longest_Rivers()
    		self.flyTo_initialize()
    		self.sendKML_ToGalaxy(kml_file, kml_name)
    		self.sendEarthOrbitFile_ToGalaxy("rivers")

    	elif use_case == "Tour Experience":
    		kml_file = generator_kml.generateKML_Tour_Experience(data_set)

    		ip_galaxy_master = self.get_galaxy_ip()
    		ip_server = self.get_server_ip()

    		self.sendKML_ToGalaxy(kml_file, kml_name)
    		time.sleep(0.75)

    		file = open("kml_tmp/query.txt", 'w+')
    		file.write("playtour=Tour Experience")
    		file.close()

    		os.system("sshpass -p 'lqgalaxy' scp " + file_query_txt_path + " lg@"+ ip_galaxy_master +":" + serverPath_query)
    		print ("Query file send!!")

    	elif use_case == "Line Track Experience":
    		kml_file = generator_kml.generateKML_Line_Track_Experience(data_set)

    		ip_galaxy_master = self.get_galaxy_ip()
    		ip_server = self.get_server_ip()

    		self.sendKML_ToGalaxy(kml_file, kml_name)
    		time.sleep(0.75)

    		file = open("kml_tmp/query.txt", 'w+')
    		file.write("playtour=Line Track Experience")
    		file.close()

    		os.system("sshpass -p 'lqgalaxy' scp " + file_query_txt_path + " lg@"+ ip_galaxy_master +":" + serverPath_query)
    		print ("Query file send!!")

    	elif use_case == "Spanish Airports":
    		kml_file = generator_kml.generateKML_Spanish_Airports()
    		self.flyTo_initialize()
    		self.sendKML_ToGalaxy(kml_file, kml_name)

    	elif use_case == "Summer Olympic Games":
    		kml_file = generator_kml.generateKML_Olympic_Games()
    		self.flyTo_initialize()
    		self.sendKML_ToGalaxy(kml_file, kml_name)
    		self.write_FlyTo_andSend(kml_file.name)

    	elif use_case == "Demo Lleida":
    		ip_galaxy_master = self.get_galaxy_ip()
    		ip_server = self.get_server_ip()

    		kml_file = generator_kml.generateKML_DemoLleida()

    		file = open("kml_tmp/kmls.txt", 'w+')
    		file.write("http://" + str(ip_server) + ":8000/static/demos/" + str(kml_name) + ".kml" + "\n")
    		file.close()

    		os.system("sshpass -p 'lqgalaxy' scp " + file_kmls_txt_path + " lg@"+ ip_galaxy_master +":" + serverPath)

    	elif use_case == "Demo Bayern":
    		ip_galaxy_master = self.get_galaxy_ip()
    		ip_server = self.get_server_ip()

    		kml_file = generator_kml.generateKML_DemoBayern()

    		with open("kml_tmp/kmls.txt", 'a') as file:
    		    		file.write("http://" + str(ip_server) + ":8000/static/demos/" + str(kml_name) + ".kml" + "\n")
    		file.close()

    		os.system("sshpass -p 'lqgalaxy' scp " + file_kmls_txt_path + " lg@"+ ip_galaxy_master +":" + serverPath)