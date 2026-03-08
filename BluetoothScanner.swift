import Foundation
import CoreBluetooth

class BluetoothScanner: NSObject, ObservableObject, CBCentralManagerDelegate {
    
    @Published var devices: [Device] = []
    
    var centralManager: CBCentralManager!
    
    override init() {
        super.init()
        centralManager = CBCentralManager(delegate: self, queue: nil)
    }
    
    func centralManagerDidUpdateState(_ central: CBCentralManager) {
        
        if central.state == .poweredOn {
            
            central.scanForPeripherals(
                withServices: nil,
                options: [CBCentralManagerScanOptionAllowDuplicatesKey: true]
            )
        }
    }
    
    func centralManager(
        _ central: CBCentralManager,
        didDiscover peripheral: CBPeripheral,
        advertisementData: [String : Any],
        rssi RSSI: NSNumber
    ) {
        
        let name = peripheral.name ?? "Unknown"
        
        if name.contains("Buds") || name.contains("Galaxy") {
            
            DispatchQueue.main.async {
                
                let device = Device(
                    name: name,
                    rssi: RSSI.intValue,
                    peripheral: peripheral
                )
                
                self.devices.append(device)
            }
        }
    }
}
