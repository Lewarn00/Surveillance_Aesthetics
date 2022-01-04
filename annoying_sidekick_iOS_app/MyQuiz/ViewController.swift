//
//  ViewController.swift
//  MyQuiz
//
//  Created by Lewis Arnsten on 10/19/21.
//
//In order to create this app I used the following AWARE iOS framework -> https://github.com/tetujin/AWAREFramework-iOS
//I had no prior knowledge of swift before beginning this assignment so I had to learn from documentation and tutorials

import UIKit
import AWAREFramework

class ViewController: UIViewController {
        
    @IBOutlet weak var XaccLabel: UILabel!
    @IBOutlet weak var YaccLabel: UILabel!
    @IBOutlet weak var ZaccLabel: UILabel!
    @IBOutlet weak var noiseLabel: UILabel!
    @IBOutlet weak var activityLabel: UILabel!
    @IBOutlet weak var addressLabel: UILabel!
    @IBOutlet weak var altLabel: UILabel!
    
    struct Keys {
        static let keyOne = "LocationsKey"
        static let keyTwo = "NumKey"
    }
    let defaults = UserDefaults.standard
    
    private func requestAuthorization(completionHandler: @escaping (_ success: Bool) -> ()) {
        UNUserNotificationCenter.current().requestAuthorization(options: [.alert, .sound, .badge]) { (success, error) in
            completionHandler(success)
        }
    }
    
    private func moveNotification() {

        let content = UNMutableNotificationContent()
        let last_location = self.defaults.string(forKey: Keys.keyOne)
        let last_num = self.defaults.string(forKey: Keys.keyTwo)

        content.title = "On The Move!"
        content.subtitle = "You have entered \(last_num!) \(last_location!)"
        content.body = "Where will we go next?"

        let trigger = UNTimeIntervalNotificationTrigger(timeInterval: 1.0, repeats: false)
        let request = UNNotificationRequest(identifier: "move_notification", content: content, trigger: trigger)
        UNUserNotificationCenter.current().add(request)
    }

    private func stopNotification() {

        let content = UNMutableNotificationContent()
        let last_location = self.defaults.string(forKey: Keys.keyOne)
        let last_num = self.defaults.string(forKey: Keys.keyTwo)

        content.title = "Sorry, I can't do that."
        content.subtitle = "You address is \(last_num!) \(last_location!)"
        content.body = "Your data is just too valuable."

        let trigger = UNTimeIntervalNotificationTrigger(timeInterval: 1.0, repeats: false)
        let request = UNNotificationRequest(identifier: "stop_notification", content: content, trigger: trigger)
        UNUserNotificationCenter.current().add(request)
    }
    
    @IBAction func stopButton(sender: UIButton) {
        UNUserNotificationCenter.current().getNotificationSettings { (settings) in
            switch settings.authorizationStatus {
            case .notDetermined:
                self.requestAuthorization(completionHandler: { (success) in
                    guard success else { return }

                    self.stopNotification()
                })
            case .authorized:
                self.stopNotification()
            case .denied:
                print("notification error")
            case .provisional:
                print("notification error")
            case .ephemeral:
                print("notification error")
            @unknown default:
                print("notification error")
            }
        }
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        UNUserNotificationCenter.current().delegate = self
        
        if let last_location = self.defaults.string(forKey: Keys.keyOne) {
            print(last_location)
        }
        if let last_num = self.defaults.string(forKey: Keys.keyTwo) {
            print(last_num)
        }
        
        AWARESensorManager.shared().syncAllSensorsForcefully()
    }

    override func viewDidAppear(_ animated: Bool) {
        
        Timer.scheduledTimer(withTimeInterval: 1, repeats: false) { (timer) in
            let manager = AWARESensorManager.shared()
            manager.setSensorEventHandlerToAllSensors { (sensor, data) in
                if let data = data {
                    let name = sensor.getName()
                    //print(sensorName)
                    
                    if SENSOR_ACCELEROMETER == name {
                        if  let x = data["double_values_0"] as? Double,
                            let y = data["double_values_1"] as? Double,
                            let z = data["double_values_2"] as? Double {
                            self.XaccLabel.text = "\(String(format: "%.2f", x))"
                            self.YaccLabel.text = "\(String(format: "%.2f", y))"
                            self.ZaccLabel.text = "\(String(format: "%.2f", z))"
                        }

                    } else if SENSOR_AMBIENT_NOISE == name {
                        if  let x = data["double_decibels"] as? Double {
                            self.noiseLabel.text = "\(String(format: "%.2f", x))"
                        }

                    } else if SENSOR_IOS_ACTIVITY_RECOGNITION == name {
                        //print(data)
                        if  let act = data["activities"] {
                            self.activityLabel.text = "\(act)"
                        }

                    } else if SENSOR_GOOGLE_FUSED_LOCATION == name {
                        //print(sensorName)
                        if let lat = data["double_latitude"] as? Double,
                           let long = data["double_longitude"] as? Double,
                           let alt = data["double_altitude"] as? Double,
                           let time = data["timestamp"] as? Double{
                            
                            self.altLabel.text = "\(String(format: "%.2f", alt))"
                            
                            func findAddress(Latitude: Double, Longitude: Double){
                                    //geolocating from latitude and longitude -> https://stackoverflow.com/questions/41358423/swift-generate-an-address-format-from-reverse-geocoding
                                    var coord : CLLocationCoordinate2D = CLLocationCoordinate2D()
                                    
                                    let coder: CLGeocoder = CLGeocoder()
                                    coord.latitude = Latitude
                                    coord.longitude = Longitude
                                    
                                    let location: CLLocation = CLLocation(latitude:coord.latitude, longitude:coord.longitude)
                                    coder.reverseGeocodeLocation(location, completionHandler:
                                        {(address_parts, error) in
                                            if (error != nil)
                                            {
                                                print("can't get address")
                                            }
                                            var full_address: String = ""
                                            var save_loc: String = ""
                                            var save_num: String = ""
                                            let addy = address_parts! as [CLPlacemark]
                                            if addy.count > 0 {
                                                let addy = address_parts![0]
                                                
                                                if addy.subThoroughfare != nil {
                                                    let last_num = self.defaults.string(forKey: Keys.keyTwo)
                                                    
                                                    full_address = full_address + addy.subThoroughfare! + ", "
                                                    save_num = save_num + addy.subThoroughfare!
                                                    if last_num != save_num{
                                                        UNUserNotificationCenter.current().getNotificationSettings { (settings) in
                                                            switch settings.authorizationStatus {
                                                            case .notDetermined:
                                                                self.requestAuthorization(completionHandler: { (success) in
                                                                    guard success else { return }

                                                                    self.moveNotification()
                                                                })
                                                            case .authorized:
                                                                self.moveNotification()
                                                            case .denied:
                                                                print("notification error")
                                                            case .provisional:
                                                                print("notification error")
                                                            case .ephemeral:
                                                                print("notification error")
                                                            @unknown default:
                                                                print("notification error")
                                                            }
                                                        }
                                                    }
                                                            
                                                    self.defaults.set(String(save_num), forKey: Keys.keyTwo)
                                                }
                                                if addy.thoroughfare != nil {
                                                    full_address = full_address + addy.thoroughfare! + ", "
                                                    save_loc = save_loc + addy.thoroughfare!
                                                    self.defaults.set(String(save_loc), forKey: Keys.keyOne)
                                                }
                                                if addy.locality != nil {
                                                    full_address = full_address + addy.locality! + ", "
                                                }
                                                if addy.country != nil {
                                                    full_address = full_address + addy.country! + ", "
                                                }
                                                if addy.postalCode != nil {
                                                    full_address = full_address + addy.postalCode! + " "
                                                }
                                                self.addressLabel.text = (String(full_address))

                                          }
                                    })
                                    //print(addressString)
                                }
                            findAddress(Latitude: lat, Longitude: long)
                        }
                    
                    } else{
                        //print(sensorName)
                        //print(data)
                    }
                }
            }

        }
    }
}

extension ViewController: UNUserNotificationCenterDelegate {

    func userNotificationCenter(_ center: UNUserNotificationCenter, willPresent notification: UNNotification, withCompletionHandler completion: @escaping (UNNotificationPresentationOptions) -> Void) {
        completion([.alert])
    }

}



