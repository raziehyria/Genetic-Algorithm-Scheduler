import Nav from "react-bootstrap/Nav";

interface Props {
  setCurrentPage: React.Dispatch<React.SetStateAction<number>>;
}

const Navigation = (props: Props) => {
  const { setCurrentPage } = props;
  return (
    <Nav
      variant="pills"
      defaultActiveKey="/"
      className="justify-content-center"
    >
      <Nav.Item>
        <Nav.Link onClick={() => setCurrentPage(0)} eventKey="/">
          Course Scheduler
        </Nav.Link>
      </Nav.Item>
      <Nav.Item>
        <Nav.Link onClick={() => setCurrentPage(1)} eventKey="link-2">
          Additional Settings
        </Nav.Link>
      </Nav.Item>
      <Nav.Item>
        <Nav.Link onClick={() => setCurrentPage(2)} eventKey="link-3">
          Help
        </Nav.Link>
      </Nav.Item>
      <Nav.Item>
        <Nav.Link onClick={() => setCurrentPage(3)} eventKey="link-4">
          About
        </Nav.Link>
      </Nav.Item>
    </Nav>
  );
};

export default Navigation;
