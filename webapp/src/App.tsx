import { useState } from "react";
import Navigation from "./components/Navigation";
import CourseSchedulerPage from "./pages/CourseScheduler";
import HelpPage from "./pages/Help";
import AboutPage from "./pages/About";
import AdditionalSettings from "./pages/AdditionalSettings";

function App() {
  // values equal to 0,1,2 or 3, corresponding to the navigation tabs
  // 0: course scheduler tab
  // 1: additional settings tab
  // 2: help tab
  // 1: about tab
  const [currentPage, setCurrentPage] = useState(0);
  return (
    <>
      <h1 className="text-center display-1 mt-5">Scheduler App</h1>
      <div className="ml-auto mr-auto vh-100 d-flex flex-column p-5 align-items-center">
        <div className="border border-primary p-5 w-75">
          <Navigation setCurrentPage={setCurrentPage} />
          {getCurrentPage(currentPage)}
        </div>
      </div>
    </>
  );
}

// Using the currentPage state, return the corresponding component to be rendered
const getCurrentPage = (pageNum: number) => {
  switch (pageNum) {
    case 0:
      return <CourseSchedulerPage />;
    case 1:
      return <AdditionalSettings />;
    case 2:
      return <HelpPage />;
    case 3:
      return <AboutPage />;
    default:
      return null;
  }
};

export default App;
