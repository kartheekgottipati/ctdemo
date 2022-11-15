import Accordion from "@mui/material/Accordion";
import AccordionDetails from "@mui/material/AccordionDetails";
import AccordionSummary from "@mui/material/AccordionSummary";
import Typography from "@mui/material/Typography";
import { Transaction as TransactionData } from "../../app/services/transaction";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import React from "react";

type TransactionProps = {
  data: TransactionData;
};

export function Transaction(props: TransactionProps) {
  const {
    data: { hash, fee, inputs, out, date },
  } = props;
  return (
    <Accordion sx={{ width: "100%" }}>
      <AccordionSummary
        expandIcon={<ExpandMoreIcon />}
        aria-controls="panel1a-content"
        id="panel1a-header"
      >
        <Typography>{hash}</Typography>
      </AccordionSummary>
      <AccordionDetails>
        <React.Fragment>
          <Typography sx={{ wordWrap: "break-word" }} component="div">
            {`Fee: ${fee}`}
            <br />
            <br />
            {`Date: ${date}`}
            <br />
            <br />
            Inputs:
            <br />
            <br />
            <pre style={{ whiteSpace: "pre-wrap" }}>
              {JSON.stringify(inputs, null, 2)}
            </pre>
            Out:
            <br />
            <br />
            <pre style={{ whiteSpace: "pre-wrap" }}>
              {JSON.stringify(out, null, 2)}
            </pre>
          </Typography>
        </React.Fragment>
      </AccordionDetails>
    </Accordion>
  );
}
