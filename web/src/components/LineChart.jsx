import { ResponsiveLine } from "@nivo/line";

const LineChart = (props) => {
  return (
    <>
      <ResponsiveLine
        curve="basis"
        data={props.data}
        enableArea={true}
        margin={{ top: 30, right: 30, bottom: 30, left: 30 }}
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
