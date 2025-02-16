import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { About } from "./components/About";

import { Footer } from "./components/Footer";
import { Hero } from "./components/Hero";
import { HowItWorks } from "./components/HowItWorks";
import { Navbar } from "./components/Navbar";
import { Newsletter } from "./components/Newsletter";

import { ScrollToTop } from "./components/ScrollToTop";
import { ReportFound } from "./components/ReportFound";


import { Team } from "./components/Team";

import { ReportLost } from "./components/ReportLost";
import "./App.css";

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={
          <>
            <Hero />
            <About />
            <HowItWorks />
      
           
           
            
            <Team />
            
            <Newsletter />
            
          </>
        } />
        <Route path="/report-lost" element={<ReportLost />} />
        <Route path="/report-found" element={<ReportFound />} />
      </Routes>
      <Footer />
      <ScrollToTop />
    </Router>
  );
}

export default App;
