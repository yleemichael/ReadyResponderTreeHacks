//
//  DataViewController.swift
//  RapidResponseSingleView
//
//  Created by Tasnim Abdalla on 15.02.19.
//  Copyright © 2019 Tasnim Abdalla. All rights reserved.
//

import Foundation
import UIKit

class DataViewController: UIViewController {
    @IBOutlet var button: UIButton!
    @IBOutlet weak var textField: UITextField!
    @IBOutlet weak var Longitude: UITextField!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        
    }
    
    
    @IBAction func buttonTapped(_ sender: UIButton) {
        if let latitudeString = textField.text, let longitudeString = Longitude.text, let latitude = Double(latitudeString), let long = Double(longitudeString) {
            let mapViewController = ViewController(lat: latitude, long: long)
            self.present(mapViewController, animated: true, completion: nil)
        }
    }
}
