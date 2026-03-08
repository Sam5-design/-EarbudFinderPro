import SwiftUI

struct ContentView: View {
    
    @StateObject var scanner = BluetoothScanner()
    @StateObject var direction = DirectionTracker()
    
    var body: some View {
        
        NavigationView {
            
            VStack {
                
                if scanner.devices.isEmpty {
                    
                    VStack(spacing: 20) {
                        
                        Text("Scanning for Earbuds...")
                            .font(.title2)
                        
                        ProgressView()
                        
                        Text("Make sure Bluetooth is on and earbuds are nearby.")
                            .font(.caption)
                            .foregroundColor(.gray)
                    }
                    
                } else {
                    
                    List(scanner.devices) { device in
                        
                        VStack(spacing: 15) {
                            
                            Text(device.name)
                                .font(.headline)
                            
                            RadarView(rssi: device.rssi)
                            
                            Text("Signal: \(device.rssi) dBm")
                            
                            Text(
                                SignalProcessor.proximityText(device.rssi)
                            )
                            
                            Text(
                                "Distance: \(String(format: "%.2f",
                                SignalProcessor.distanceFromRSSI(Double(device.rssi)))) m"
                            )
                            
                            Image(systemName: "location.north.fill")
                                .font(.system(size: 40))
                                .rotationEffect(.radians(direction.heading))
                                .foregroundColor(.red)
                        }
                        .padding()
                    }
                }
            }
            .navigationTitle("Earbud Finder")
        }
    }
}
