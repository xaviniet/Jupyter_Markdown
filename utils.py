


class SinCosTransformer(BaseEstimator,TransformerMixin):
    def __init__(self):
#         print('SinCosTransformer init() called\n')
        return
    
    def fit(self, X, columns=['hour']):
        self.columns = columns
        self.name = X.name
        return self
    
    def transform(self, X):
        df = pd.DataFrame()
        for col in self.columns:
            data = getattr(X.dt,col)
            freq = (data.max() - data.min())+1
            sin_ = np.sin(2 * np.pi * data/freq)
            sin_.name = self.name + '_' + col + '_sin'
            cos_ = np.cos(2 * np.pi * data/freq) 
            cos_.name = self.name + '_' + col + '_cos'
            df = pd.concat([df,sin_,cos_], axis=1)
        return df

        

