import HeroSection from "../components/dashboard/HeroSection.jsx";
import SystemOverview from "../components/dashboard/SystemOverview.jsx";
import TheoryAccessPanel from "../components/dashboard/TheoryAccessPanel.jsx";
import MotionSection from "../components/animations/MotionSection.jsx";

export default function HomePage() {
  return (
    <div className="space-y-6">
      <HeroSection />
      <MotionSection>
        <TheoryAccessPanel />
      </MotionSection>
      <MotionSection delay={0.05}>
        <SystemOverview />
      </MotionSection>
    </div>
  );
}
