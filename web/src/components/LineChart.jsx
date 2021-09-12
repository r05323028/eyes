import { ResponsiveLine } from "@nivo/line";

const LineChart = (props) => {
  return (
    <>
      <ResponsiveLine
        curve="basis"
        data={props.data}
        enableArea={true}
        axisBottom={{
          tickRotation: -45,
          legend: "date",
          legendPosition: "middle",
          orient: "bottom",
          legendOffset: 65,
        }}
        margin={{ top: 30, right: 30, bottom: 75, left: 65 }}
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
