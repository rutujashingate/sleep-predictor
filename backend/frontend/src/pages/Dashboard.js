import React, { useState } from 'react';
import InputForm from '../components/InputForm';
import SleepImpactChart from '../components/SleepImpactChart'; // Chart
import { Box, Typography } from '@mui/material';

const Dashboard = () => {
  const [result, setResult] = useState(null);

  const handleResult = (result) => {
    console.log("Received result from backend:", result);
    setResult(result);
  };

  return (
    <Box sx={{ p: 4 }}>
      <Typography variant="h4" gutterBottom>
        💤 Sleep Quality Predictor
      </Typography>

      <InputForm onResult={handleResult} />

      {result && (
        <Box sx={{ mt: 4 }}>
          <Typography variant="h6">Prediction: {result.prediction}</Typography>

          {/*  Suggestions */}
          {result.suggestions && (
            <Box sx={{ mt: 2 }}>
              <Typography variant="subtitle1">Suggestions:</Typography>
              <ul>
                {result.suggestions.map((tip, i) => (
                  <li key={i}>{tip}</li>
                ))}
              </ul>
            </Box>
          )}

          {/* Chart with SHAP impact */}
          {result.important_features && (
            <SleepImpactChart data={result.important_features} />
          )}
        </Box>
      )}
    </Box>
  );
};

export default Dashboard;
