import React, { useState } from 'react';
import { TextField, Button, Box, Grid, MenuItem } from '@mui/material';

const labelMap = {
  age: "Age",
  gender: "Gender",
  stress_score: "Stress Score",
  screen_time_before_bed_min: "Screen Time Before Bed (min)",
  step_count_day: "Steps per Day",
  sleep_stage_deep_pct: "Deep Sleep (%)",
  sleep_stage_light_pct: "Light Sleep (%)",
  sleep_efficiency: "Sleep Efficiency (%)"
};

const InputForm = ({ onResult }) => {
  const [formData, setFormData] = useState({
    age: 25,
    gender: "female",
    stress_score: 6.5,
    screen_time_before_bed_min: 45,
    step_count_day: 5000,
    sleep_stage_deep_pct: 15.0,
    sleep_stage_light_pct: 50.0,
    sleep_efficiency: 82.0
  });

  const handleChange = (e) => {
    const { name, value } = e.target;

    setFormData(prev => ({
      ...prev,
      [name]: name === "gender" ? value : parseFloat(value)
    }));
  };

  const handleSubmit = async () => {
    console.log("Submitting this data:", formData);

    try {
      const response = await fetch("http://127.0.0.1:8000/predict_smartwatch", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(formData)
      });

      const result = await response.json();
      console.log("Backend result:", result);
      onResult(result);
    } catch (error) {
      console.error("Prediction error:", error);
    }
  };

  return (
    <Box component="form" sx={{ mt: 2 }}>
      <Grid container spacing={2}>
        {Object.entries(formData).map(([key, value]) => (
          <Grid item xs={12} sm={6} md={4} key={key}>
            {key === "gender" ? (
              <TextField
                select
                label={labelMap[key]}
                name={key}
                value={value}
                onChange={handleChange}
                fullWidth
                variant="outlined"
                size="small"
              >
                <MenuItem value="male">Male</MenuItem>
                <MenuItem value="female">Female</MenuItem>
                <MenuItem value="other">Other</MenuItem>
              </TextField>
            ) : (
              <TextField
                label={labelMap[key]}
                name={key}
                type="number"
                value={value}
                onChange={handleChange}
                fullWidth
                variant="outlined"
                size="small"
              />
            )}
          </Grid>
        ))}
      </Grid>

      <Button variant="contained" color="primary" sx={{ mt: 3 }} onClick={handleSubmit}>
        Predict
      </Button>
    </Box>
  );
};

export default InputForm;
