import { useState, useEffect } from 'react'
import ProgressBar from "react-bootstrap/ProgressBar";
import UploadForm from '../components/UploadForm'
import Download from "../components/Download";
import InProgress from "../components/InProgress";

const CourseSchedulerPage = () => {
  const [showProgress, setShowProgress] = useState(false);
  const [progressPercent, setProgressPercent] = useState(0);
  const [showDownload, setShowDownload] = useState(false);


  // if we are showing the download button, set the completion percent to 100
  useEffect(() => {
    if (showDownload) {
      setProgressPercent(100);
    }
  }, [setProgressPercent, showDownload]);

  return (
    <div>
      {!showDownload && (
        <UploadForm
          showProgress={showProgress}
          setShowProgress={setShowProgress}
          showDownload={showDownload}
          setShowDownload={setShowDownload}
          progressPercent={progressPercent}
          setProgressPercent={setProgressPercent}
        />
      )}
      {showProgress && <InProgress />}
      {showDownload && <Download />}
      {(showProgress || showDownload) && (
        <ProgressBar
          className="mt-3"
          now={progressPercent}
          label={`${progressPercent}%`}
        />
      )}
    </div>
  );
};

export default CourseSchedulerPage;
