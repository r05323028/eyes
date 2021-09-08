import { ResponsiveLine } from "@nivo/line";

const LineChart = (props) => {
  return (
    <>
      <ResponsiveLine
        curve="basis"
        data={props.data}
        enableArea={true}
        useMesh={false}
        colors={{ scheme: "nivo" }}
        enablePoints={false}
        enableGridX={false}
        enableGridY={false}
      />
    </>
  );
};

export default LineChart;
