//
//  AppDelegate.swift
//  MyQuiz
//
//  Created by Lewis Arnsten on 10/19/21.
//
//In order to create this app I used the following AWARE iOS framework -> https://github.com/tetujin/AWAREFramework-iOS

import UIKit
import CoreData
import AWAREFramework

@UIApplicationMain

class AppDelegate: UIResponder, UIApplicationDelegate {

    var window: UIWindow?
    var sensingStatus = true
    let sensorManager = AWARESensorManager.shared()
    
    func application(_ application: UIApplication, didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?) -> Bool {

        let core = AWARECore.shared()
        let manager = AWARESensorManager.shared()
        
        core.requestPermissionForBackgroundSensing { (status) in
            core.requestPermissionForPushNotification(completion: nil)
            core.activate()
            
            let acceleration = Accelerometer()
            let IOSactivity = IOSActivityRecognition()
            let noise  = AmbientNoise()
            
            let location = FusedLocations()
            manager.add(location)
            //location.setSensorEventHandler { (sensor, data) in
            //    if let data = data {
            //        print(data)
            //    }
            //}
            location.saveAll = true
            location.startSensor()
            
           // manager.add(IOSactivity)
            //IOSactivity.startSensor()
            //IOSactivity.setSensorEventHandler { (sensor, data) in
            //    if let data = data {
            //        print(data)
            //    }
            //}

            self.sensorManager.add([acceleration, IOSactivity, noise])
            self.sensorManager.startAllSensors()
        }
    
        AWAREEventLogger.shared().logEvent(["class":"AppDelegate",
                                            "event":"application:didFinishLaunchingWithOptions:launchOptions"])
        AWAREStatusMonitor.shared().activate(withCheckInterval: 1)
        
        return true
    }

    func applicationWillResignActive(_ application: UIApplication) {
        AWAREEventLogger.shared().logEvent(["class":"AppDelegate",
                                            "event":"applicationWillResignActive"])
    }

    func applicationDidEnterBackground(_ application: UIApplication) {
        AWAREEventLogger.shared().logEvent(["class":"AppDelegate",
                                            "event":"applicationDidEnterBackground"])
    }

    func applicationWillEnterForeground(_ application: UIApplication) {
        AWAREEventLogger.shared().logEvent(["class":"AppDelegate",
                                            "event":"applicationWillEnterForeground"])
    }

    func applicationDidBecomeActive(_ application: UIApplication) {
        AWAREEventLogger.shared().logEvent(["class":"AppDelegate",
                                            "event":"applicationDidBecomeActive"])
    }

    func applicationWillTerminate(_ application: UIApplication) {
        AWAREEventLogger.shared().logEvent(["class":"AppDelegate",
                                            "event":"applicationWillTerminate"])
        self.saveContext()
    }

    lazy var persistentContainer: NSPersistentContainer = {

        let container = NSPersistentContainer(name: "AWARE_Sidekick")
        container.loadPersistentStores(completionHandler: { (storeDescription, error) in
            if let error = error as NSError? {
                fatalError("error")
            }
        })
        return container
    }()

    func saveContext () {
        let context = persistentContainer.viewContext
        if context.hasChanges {
            do {
                try context.save()
            } catch {
                fatalError("error")
            }
        }
    }

}


