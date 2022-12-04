import downloadSvg from "../download.svg";

const Download = () => {
  return (
    <div className="text-center mt-5 pt-5">
      <h1 className="mt-5 mb-5">Schedule Generation Complete!</h1>
      <a
        href="http://localhost:5000/download"
        className="btn btn-outline-primary mx-auto mt-5 mb-5"
      >
        Click here to download
        <img
          style={{
            width: 20,
            marginLeft: 5,
          }}
          src={downloadSvg}
          alt="download icon"
        />
      </a>
    </div>
  );
};

export default Download;
