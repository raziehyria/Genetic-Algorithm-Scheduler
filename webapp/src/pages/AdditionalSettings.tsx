import { useEffect, useState } from "react";
const AdditionalSettings = () => {
  const initialRangeData = {
    populationSize: 23,
    numOfEliteSchedules: 2,
    mutationRate: 0.002,
    tournamentSelectionSize: 7,
    maxIteration: 600,
  };
  const [rangeData, setRangeData] = useState(initialRangeData);

  const {
    populationSize,
    numOfEliteSchedules,
    mutationRate,
    tournamentSelectionSize,
    maxIteration,
  } = rangeData;


  const handleOnChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setRangeData({
      ...rangeData,
      [e.target.id]: Number(e.target.value),
    });
  };

  // Everytime the additional settings rangeData value changes, upload
  // that information to flask
  useEffect(() => {
    fetch("http://localhost:5000/additional-settings", {
      method: "POST",
      body: JSON.stringify(rangeData),
      headers: {
        "content-type": "application/json",
      },
    });
  }, [rangeData]);

  return (
    <div className="ms-5">
      <div className="d-flex align-items-center mt-5">
        <label className="form-label pe-3 w-25">Population Size</label>
        <input
          onChange={handleOnChange}
          id="populationSize"
          type="range"
          className="form-range w-50"
          min="1"
          max="200"
          step="1"
          value={populationSize}
        />
        <output className="ms-3">{populationSize}</output>
      </div>

      <div className="d-flex align-items-center mt-5">
        <label className="form-label pe-3 w-25"># Of Elite Schedules</label>
        <input
          onChange={handleOnChange}
          value={numOfEliteSchedules}
          id="numOfEliteSchedules"
          type="range"
          className="form-range w-50"
          min="1"
          max="5"
          step="1"
        />
        <output className="ms-3">{numOfEliteSchedules}</output>
      </div>

      <div className="d-flex align-items-center mt-5">
        <label className="form-label pe-3 w-25">Mutation Rate</label>
        <input
          onChange={handleOnChange}
          value={mutationRate}
          id="mutationRate"
          type="range"
          className="form-range w-50"
          min="0.001"
          max="0.005"
          step="0.001"
        />
        <output className="ms-3">{mutationRate}</output>
      </div>

      <div className="d-flex align-items-center mt-5">
        <label className="form-label pe-3 w-25">
          Tournament Selection Size
        </label>
        <input
          onChange={handleOnChange}
          value={tournamentSelectionSize}
          id="tournamentSelectionSize"
          type="range"
          className="form-range w-50"
          min="1"
          max="10"
          step="1"
        />
        <output className="ms-3">{tournamentSelectionSize}</output>
      </div>

      <div className="d-flex align-items-center mt-5">
        <label className="form-label pe-3 w-25">Max Iteration</label>
        <input
          onChange={handleOnChange}
          value={maxIteration}
          id="maxIteration"
          type="range"
          className="form-range w-50"
          min="1"
          max="600"
          step="1"
        />
        <output className="ms-3">{maxIteration}</output>
      </div>
    </div>
  );
};

export default AdditionalSettings;
