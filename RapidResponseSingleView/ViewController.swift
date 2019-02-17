//
//  ViewController.swift
//  RapidResponseSingleView
//
//  Created by Tasnim Abdalla on 14.02.19.
//  Copyright © 2019 Tasnim Abdalla. All rights reserved.
//

import UIKit
import UIKit
import GoogleMaps
import Alamofire
import SwiftyJSON

class ViewController: UIViewController {

    private let latitude: Double
    private let longitude: Double
    private var mapView: GMSMapView!
    
    init(lat: Double, long: Double) {
        latitude = lat
        longitude = long
        
        super.init(nibName: nil, bundle: nil)
    }
    
    required init?(coder aDecoder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
        route()
        setupMapView()
    }
    
    func setupMapView() {
        // Create a GMSCameraPosition that tells the map to display the
        // coordinate -33.86,151.20 at zoom level 6.
        let camera = GMSCameraPosition.camera(withLatitude: latitude, longitude: longitude, zoom: 6.0)
        mapView = GMSMapView.map(withFrame: CGRect.zero, camera: camera)
        self.view.insertSubview(mapView, at: 0)
        mapView.frame = view.frame
        
        // Creates a marker in the center of the map.
        let marker = GMSMarker()
        marker.position = CLLocationCoordinate2D(latitude: latitude, longitude: longitude)
        marker.title = "Boulder"
        marker.snippet = "Colorado"
        marker.map = mapView
    }
    
    private func route() {
        Alamofire.request("https://maps.googleapis.com/maps/api/directions/json",
                          method: .get,
                          parameters: ["origin": "40.029822, -105.228440", "destination": "40.0163695, -105.236388200", "key": "AIzaSyDhitCSzfdMQOySe9bdGAdRB9EhedBimwE"],
                          encoding: URLEncoding.default).responseJSON { (response) in
                            if let json = response.result.value {
                                print(JSON(json)["routes"][0])
                                JSON(json)["routes"][0]["legs"][0]["steps"]
                                
                                if let encodedPolyline = JSON(json)["routes"][0]["overview_polyline"]["points"].string/*, let mapView = self.mapView as? GMSMapView*/ {
                                    if let path = GMSPath(fromEncodedPath: encodedPolyline) {
                                        let polyline = GMSPolyline(path: path)
                                        
                                        var bounds = GMSCoordinateBounds()
                                        for index in 1...path.count() {
                                            bounds = bounds.includingCoordinate(path.coordinate(at: index))
                                        }
                                        self.mapView.animate(with: GMSCameraUpdate.fit(bounds))
                                        polyline.strokeWidth = 10
                                        polyline.map = self.mapView
                                    }
                                }
                            }
        }
        
    }
    
    @IBAction func showGoogleMaps(_ sender: AnyObject) {
        
    }

}

