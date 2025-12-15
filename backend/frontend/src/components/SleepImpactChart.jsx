import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Legend } from 'recharts';
import { Box, Typography } from '@mui/material';

const SleepImpactChart = ({ data }) => {
  if (!data || data.length === 0) return null;

  return (
    <Box sx={{ mt: 4 }}>
      <Typography variant="h6" gutterBottom>
        Top Features Impacting Sleep Quality
      </Typography>
      <ResponsiveContainer width="90%" height={300}>
        <BarChart data={data} layout="vertical" margin={{ left: 120 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis type="number" />
          <YAxis dataKey="feature" type="category" />
          <Tooltip />
          <Legend />
          <Bar dataKey="impact" fill="#1976d2" name="Impact" />
        </BarChart>
      </ResponsiveContainer>
    </Box>
  );
};

export default SleepImpactChart;
