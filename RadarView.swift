import SwiftUI

struct RadarView: View {
    
    var rssi: Int
    
    var body: some View {
        
        ZStack {
            
            Circle().stroke(lineWidth: 2).opacity(0.3)
            Circle().stroke(lineWidth: 2).scaleEffect(0.7).opacity(0.3)
            Circle().stroke(lineWidth: 2).scaleEffect(0.4).opacity(0.3)
            
            Circle()
                .fill(Color.green)
                .frame(width: dotSize(), height: dotSize())
        }
        .frame(width: 220, height: 220)
    }
    
    func dotSize() -> CGFloat {
        
        let strength = max(-90, rssi)
        let normalized = Double(strength + 90) / 60
        
        return CGFloat(20 + normalized * 70)
    }
}
