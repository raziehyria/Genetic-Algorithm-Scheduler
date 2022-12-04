import Spinner from './Spinner'

const InProgress = () => {
  return (
    <div className="container text-center">
      <h1>Generating schedules...</h1>
      <Spinner />
    </div>
  );
};

export default InProgress;
