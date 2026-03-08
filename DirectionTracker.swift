import Foundation
import CoreMotion

class DirectionTracker: ObservableObject {
    
    private let motionManager = CMMotionManager()
    
    @Published var heading: Double = 0
    
    init() {
        
        motionManager.deviceMotionUpdateInterval = 0.2
        
        motionManager.startDeviceMotionUpdates(to: .main) { data, _ in
            
            guard let motion = data else { return }
            
            self.heading = motion.attitude.yaw
        }
    }
}
