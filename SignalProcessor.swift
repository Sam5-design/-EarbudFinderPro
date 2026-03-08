import Foundation

class SignalProcessor {
    
    static func distanceFromRSSI(_ rssi: Double) -> Double {
        
        let txPower = -59.0
        let n = 2.0
        
        return pow(10.0, (txPower - rssi) / (10 * n))
    }
    
    static func proximityText(_ rssi: Int) -> String {
        
        if rssi > -50 { return "🔥 Very Close" }
        if rssi > -65 { return "🟡 Nearby" }
        if rssi > -80 { return "❄️ Far" }
        
        return "Searching..."
    }
}
