import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
from sklearn import linear_model
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import KFold
from sklearn.metrics import r2_score


def make_states_visual():
    """ Displays a visual of the Black population percentage for each
    US state over the years 1790-2018, and 2030-2050 for MA, CA, OH and TX.
    """
    # loading dataframe
    df_population = pd.read_csv('reformatted_percent_black_over_time2.csv')

    # replacing NaN values with -1
    df_population = df_population.fillna("-1%")
    df_population

    # states in the US
    # source = github
    states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
    }

    df_states = df_population['State/Territory']
    full_state_names = list()

    # removing territories from the df
    for idx,place in enumerate(df_states):
        if place not in states.keys():
            df_population.drop(idx, axis=0, inplace=True)
        else:
            # keep the state
            full_state_names.append(states[place])

    # store unabbreviated version of state name
    df_population['State Name'] = full_state_names

    pop_buckets = list()

    # putting Population Percentage into 'buckets'
    for pop_percent in df_population['Population Percentage']:
        type_pop = type(pop_percent)

        # convert to a float
        if type_pop == str:
            pop_percent = float(pop_percent[:-1])
        else:
            pop_percent = float(pop_percent)

        # determine which bucket it should be placed in
        if pop_percent == -1:
            pop_buckets.append("Unknown")
        elif pop_percent <= 10:
            pop_buckets.append("0 - 10 %")
        elif pop_percent <= 20:
            pop_buckets.append("11 - 20 %")
        elif pop_percent <= 30:
            pop_buckets.append("21 - 30 %")
        elif pop_percent <= 40:
            pop_buckets.append("31 - 40 %")
        elif pop_percent <= 50:
            pop_buckets.append("41 - 50 %")
        elif pop_percent <= 60:
            pop_buckets.append("51 - 60 %")
        elif pop_percent <= 70:
            pop_buckets.append("61 - 70 %")
        elif pop_percent <= 80:
            pop_buckets.append("71 - 80 %")
        elif pop_percent <= 90:
            pop_buckets.append("81 - 90 %")
        else:
            pop_buckets.append("91 - 100 %")

    # Add buckets to original dataframe
    df_population['Population Percentage Range'] = pop_buckets

    # sort Year column in ascending order
    df_population =df_population.sort_values("Year")

    # choropleth map by U.S. States
    fig = px.choropleth(df_population,
                        locations='State/Territory', 
                        locationmode="USA-states", 
                        scope="usa",
                        color='Population Percentage Range',
                        color_discrete_sequence=px.colors.qualitative.Bold,
                        animation_frame='Year',
                        hover_name='State Name', 
                        hover_data=['Population Percentage']
                        )

    # adding title to map
    fig.update_layout(
        title_text = 'Percentage of Black Population by State (1790-2018). Extrapolated to 2050 for MA, CA, OH, and TX',
        title_font_family = "Times New Roman"
    )

    fig.show()


def lasso_model():
    """ Creates and fits a Lasso model using state_demographics.csv, 
    cross-validating the data before making predictions
    
    Retuns:
        lreg (Lasso model): the linear lasso regression model after cross-validation 
        mse (float): the model's Mean Squared Error (MSE)
        r2 (float): the model's r2 score
        df_state_demo (pd.DataFrame): the updated state demographics dataframe, without
                                      features whose coefficient is == 0
    """
    # loading dataframe
    df_state_demo = pd.read_csv('state_demographics.csv')

    # only including int/float columns
    x_feat_list = list(df_state_demo.columns)
    x_feat_list.remove("State")
    x_feat_list.remove("Ethnicities.Black Alone") # removing the y_feat

    # setting the x and y values
    x = df_state_demo.loc[:, x_feat_list].values
    y = df_state_demo.loc[:, "Ethnicities.Black Alone"].values

    # initialization of models
    lreg = linear_model.Lasso(alpha=0.1) # 0.5 chosen for mid-range penalization 
    skfold = KFold(n_splits=20, shuffle=True)

    # to store predictions
    y_pred = np.empty(y.shape)

    # cross validation
    for train_idx, test_idx in skfold.split(x, y):
        # split into train and test sets
        x_train = x[train_idx, :]
        y_train = y[train_idx]
        x_test = x[test_idx, :]

        # fit Lasso on training set
        lreg.fit(x_train, y_train)

        # predicting
        y_pred[test_idx] = lreg.predict(x_test)

    # calculating important metrics
    mse = np.mean((y_pred - y) ** 2)
    r2 = r2_score(y, y_pred)

    # Now doing it on the full dataset
    # fitting the model
    lreg.fit(x,y)

    # coefficients 
    lreg_coefs = list(lreg.coef_)

    # to store feature/coef pairs
    answer_dict = {}

    for lreg_coef, x_feat in zip(lreg_coefs, x_feat_list):
        # only keeping features whose coefficient is of value (i.e not 0)
        if (lreg_coef != 0):
            answer_dict[x_feat] = lreg_coef
        else:
            df_state_demo = df_state_demo.drop(x_feat, axis=1)

    return lreg, mse, r2, df_state_demo


def make_corr_plt(df_state_demo, title):
    """ Creates and displays a feature correlation graph.

    Args:
        df_state_demo (pd.DataFrame): the dataframe holding
                            information about state demographics. 
        title (string): the title of the graph
    """

    # calculating the correlation between features
    corr = df_state_demo.corr()

    # creating the heatmap
    ax = plt.axes()
    sns.heatmap(
        corr, ax=ax,
        vmin=-1, vmax=1, center=0,
        cmap=sns.diverging_palette(20, 220, n=200),
        square=True
    )

    # changing the default style
    sns.set_style('whitegrid')

    # labelling the graph
    plt.title(title)
    ax.set_xticklabels(
        ax.get_xticklabels(),
        rotation=45,
        horizontalalignment='right'
    );


def feat_corr_before():
    """ Displays a visual of the correlation between the initial 46 features
    in state_demographics.csv. This is pre-Lasso model.
    """
    # loading dataframe
    df_state_demo = pd.read_csv('state_demographics.csv')
    make_corr_plt(df_state_demo, title="Correlation of State Demographics before Feature Engineering")


def feat_corr_after():
    """ Displays a visual of the correlation between features
    in state_demographics.csv. This is post-Lasso model.
    """
    df_state_demo = lasso_model()[3]
    make_corr_plt(df_state_demo, title="Correlation of State Demographics after Feature Engineering")