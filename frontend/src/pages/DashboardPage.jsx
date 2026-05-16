import { ArrowUpRight } from "lucide-react";
import { Link } from "react-router-dom";
import DashboardStats from "../components/dashboard/DashboardStats.jsx";
import ProcessPipeline from "../components/dashboard/ProcessPipeline.jsx";
import SystemOverview from "../components/dashboard/SystemOverview.jsx";
import TheoryAccessPanel from "../components/dashboard/TheoryAccessPanel.jsx";
import Button from "../components/ui/Button.jsx";
import PageHeader from "../components/ui/PageHeader.jsx";

export default function DashboardPage() {
  return (
    <div className="space-y-6">
      <PageHeader
        eyebrow="Dashboard operativo"
        title="Control inteligente de reciclaje"
        description="Vista inicial para supervisar clasificación, arquitectura modular, métricas operativas y acceso a la documentación teórica del proyecto."
        action={
          <Button as={Link} to="/theory">
            Ver teoría ML
            <ArrowUpRight aria-hidden="true" size={18} />
          </Button>
        }
      />
      <DashboardStats />
      <ProcessPipeline />
      <TheoryAccessPanel />
      <SystemOverview />
    </div>
  );
}
