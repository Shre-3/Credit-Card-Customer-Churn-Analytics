import { useState } from "react";

import { Layout } from "./components/Layout";
import { BusinessImpactPage } from "./pages/BusinessImpactPage";
import { CustomerPage } from "./pages/CustomerPage";
import { EdaPage } from "./pages/EdaPage";
import { ModelPage } from "./pages/ModelPage";
import { PredictionPage } from "./pages/PredictionPage";

const pageComponents = {
  eda: <EdaPage />,
  model: <ModelPage />,
  customer: <CustomerPage />,
  prediction: <PredictionPage />,
  business: <BusinessImpactPage />,
};

export default function App() {
  const [activePage, setActivePage] = useState("eda");

  return (
    <Layout activePage={activePage} onPageChange={setActivePage}>
      {pageComponents[activePage]}
    </Layout>
  );
}
