from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd
import numpy as np



class SinCosTransformer(BaseEstimator,TransformerMixin):
    def __init__(self, cycles=['hour']):
        self.cycles = cycles 
    
    def fit(self, X, y=None):
        
        if isinstance(X, pd.DataFrame):
            self.columns = X.columns
            self.series_ = None
        else:    
            self.name = X.name
            self.columns = [X.name]
            self.series_ = True
        return self
    
    def transform(self, X):
        dfs = []
        for col in self.columns:
            
            df = pd.DataFrame()
            
            for cycle in self.cycles:
                if self.series_:
                    data = getattr(X.dt,cycle)
                else: 
                    data = getattr(X[col].dt,cycle)

                freq = (data.max() - data.min())+1
                sin_ = np.sin(2 * np.pi * data/freq)
                sin_.name = col + '_' + cycle + '_sin'
                cos_ = np.cos(2 * np.pi * data/freq) 
                cos_.name = col + '_' + cycle + '_cos'
                df = pd.concat([df,sin_,cos_], axis=1)
            dfs.append(df)
        dfs_conc = pd.concat(dfs, axis=1)
        return dfs_conc


