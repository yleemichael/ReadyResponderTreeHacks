//
//  HeatMapViewController.swift
//  RapidResponseSingleView
//
//  Created by Tasnim Abdalla on 16.02.19.
//  Copyright © 2019 Tasnim Abdalla. All rights reserved.
//

import UIKit
import ArcGIS

class HeatMapViewController: UIViewController {
    
    @IBOutlet weak var mapView: AGSMapView!
    @IBAction func scanButton (sender: UIButton!) {
        
        performSegue(withIdentifier:"nextView", sender: self)
        
    }
    
    private func setupMap(itemID: String) {
        
        let portal = AGSPortal(url: URL(string: "https://www.arcgis.com")!, loginRequired: false)
        let portalItem:AGSPortalItem = AGSPortalItem(portal: portal, itemID: itemID)
        mapView.map = AGSMap(item: portalItem)
       
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        setupMap(itemID: "7a90bb89e6454b2199d4938831f9f73c")
    }
}
