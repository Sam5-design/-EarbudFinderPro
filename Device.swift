import Foundation
import CoreBluetooth

struct Device: Identifiable {
    
    let id = UUID()
    
    var name: String
    var rssi: Int
    var peripheral: CBPeripheral
}
