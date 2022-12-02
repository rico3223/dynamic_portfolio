#Definition of variables

cross_val = {
    'fold_length' : 252, # Wordking days for 1 year
    'fold_stride' : 1, # Slices between FOLDS : 1 = 1 day
    'train_test_ratio' : 0.7, # Percentage of
    'input_length' : 30, # Number of day
    'horizon' : 1, # Gap = horizon - 1
    'output_length' : 1, # Number of targets wanted
    'stride' : 1, #
    'TARGET' : ['return'], #
}
