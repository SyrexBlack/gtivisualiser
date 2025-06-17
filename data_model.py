"""Data model for loading and filtering time-depth datasets."""

from __future__ import annotations

import pandas as pd
import numpy as np


class DataModel:
    """Load and filter GTI data from Excel or CSV files."""

    def __init__(self) -> None:
        self.data: pd.DataFrame | None = None

    @staticmethod
    def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df.columns = [c.strip().lower().replace(" ", "") for c in df.columns]
        df = df.rename(columns={"time": "время", "depth": "глубина"})
        return df

    def load(self, path: str) -> None:
        """Load data from Excel or CSV."""
        if path.lower().endswith(('.xls', '.xlsx')):
            df = pd.read_excel(path)
        elif path.lower().endswith('.csv'):
            df = pd.read_csv(path)
        else:
            raise ValueError("Unsupported file format")
        df = self._normalize_columns(df)
        for col in df.select_dtypes(include=['datetime']).columns:
            df[col] = df[col].astype('int64') // 10 ** 9
        self.data = df

    def filter_time(self, start: float | None, end: float | None) -> pd.DataFrame:
        if self.data is None:
            raise RuntimeError("No data loaded")
        df = self.data
        if start is not None:
            df = df[df['время'] >= start]
        if end is not None:
            df = df[df['время'] <= end]
        return df

