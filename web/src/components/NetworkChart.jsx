import { Sigma, ForceAtlas2, RandomizeNodePositions } from "react-sigma";

const NetworkChart = (props) => {
  const { nodes, edges } = props;
  return (
    <>
      <Sigma
        settings={{
          drawEdges: true,
          defaultLabelColor: "#ffffff",
        }}
        graph={{ nodes, edges }}
        style={{ maxWidth: "inherit", height: "500px" }}
      >
        <RandomizeNodePositions>
          <ForceAtlas2 />
        </RandomizeNodePositions>
      </Sigma>
    </>
  );
};

export default NetworkChart;
