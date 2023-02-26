import src.OwlControllerPython as owl

m: owl.AirplaneManager = owl.get_airplane_manager()
m.flush()
a: owl.AirplaneController = m.get_airplane("127.0.0.1")
m.start()
a.mode(owl.AirplaneModeEnum.CommonMode)
a.takeoff(50)
a.forward(100)
m.sleep(1000)
a.back(100)
m.sleep(1000)
a.land()
m.destroy()