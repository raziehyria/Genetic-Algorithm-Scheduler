import { useState, useEffect, ChangeEvent } from 'react'
interface Props {
  showDownload: boolean;
  showProgress: boolean;
  progressPercent: number;
  setShowProgress: React.Dispatch<React.SetStateAction<boolean>>;
  setShowDownload: React.Dispatch<React.SetStateAction<boolean>>;
  setProgressPercent: React.Dispatch<React.SetStateAction<number>>;
}

const UploadForm = (props: Props) => {
  const {
    showProgress,
    setShowProgress,
    showDownload,
    setShowDownload,
    setProgressPercent,
  } = props;

  // The file to be uploaded to the flask server
  const [file, setFile] = useState<File>();

  const handleStopBtnClick = async () => {
    await fetch("http://localhost:5000/stop");
    setShowProgress(false);
    setShowDownload(true);
  };

  // Runs everytime the file input value changes
  const handleOnFileChange = (event: ChangeEvent<HTMLInputElement>) => {
    const htmlInputElement = event.target;

    // if the html Input element has a file uploaded
    if (htmlInputElement.files) {
      // The actual file the user uploaded
      const uploadedFile = htmlInputElement.files[0];
      setFile(uploadedFile);
    }
  };

  const handleOnSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    // Stops default HTML form behavior from reloading the page
    event.preventDefault();

    // Show the `InProgress` component
    setShowProgress(true);

    // If there is a file to upload to the flask server
    if (file) {
      let formData = new FormData();
      formData.append("file", file);

      try {
        // Send HTTP Post request to the flask server, with the file as a payload
        await fetch("http://localhost:5000/upload", {
          method: "POST",
          body: formData,
        });

        await handleStopBtnClick();
      } catch (e) {
        console.log(e);
      }
    }
  };

  useEffect(() => {
    let keepCheckingProgress: any;
    if (showProgress) {
      keepCheckingProgress = setInterval(() => {
        fetch("http://localhost:5000/get-progress-percent")
          .then((response) => {
            return response.json();
          })
          .then((data) => {
            if (data.progress) {
              setProgressPercent(Number(data.progress));
            }
          });
      }, 500);
    }

    return () => {
      clearInterval(keepCheckingProgress);
    };
  }, [showProgress, setProgressPercent]);

  return (
    <div className="container mt-5">
      <div className="mb-3">
        <form
          className="text-center"
          encType="multipart/form-data"
          onSubmit={handleOnSubmit}
        >
          <label htmlFor="formFile" className="form-label">
            Select Input Excel File
          </label>
          <input
            onChange={handleOnFileChange}
            className="form-control"
            type="file"
            name="file"
            id="formFile"
          />
          {showProgress ? (
            <button
              type="button"
              className="mt-3 mb-5 w-25 btn btn-outline-danger"
              onClick={handleStopBtnClick}
            >
              Stop
            </button>
          ) : (
            <button
              type="submit"
              className="mt-3 mb-5 w-25 btn btn-outline-primary"
            >
              Upload
            </button>
          )}
        </form>
      </div>
    </div>
  );
};

export default UploadForm
