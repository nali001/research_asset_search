{"cells":[{"metadata":{},"cell_type":"markdown","source":"# **About this notebook**\nThis notebook consists of domain knowledge about the prostatce cancer as well predictive analytics.\n\n**If you find this kernel useful, Please consider upvoting it, It motivates me to write more quality content.**\n# **What is prostate cancer?**\nProstate cancer is the most common cancer after skin cancer in men in the United States. Also, it is the third leading cause of cancer death, behind lung cancer and colon cancer, in men in the United States. About 1 man in 41 will die of prostate cancer. In some men, it is slow growing and unlikely to cause serious problems. In others, the disease is very aggressive. About 1 man in 9 will be diagnosed with prostate cancer during his lifetime. \n\nProstate cancer starts in the prostate, a gland located below the bladder and in front of the rectum. \n* The prostate contains several types of cells, but nearly all prostate cancers develop from glandular cells, which make fluid that becomes part of semen.\n* Prostate cancer cells can spread by invading nearby organs and tissues, such as the bladder or rectum, or by travelling through the blood or lymph to other parts of the body. This is known as metastatic prostate cancer.\n* Other than the lymph nodes near the prostate, the most common site of prostate cancer spread, or metastatis, is the bones, especially in the spine.\n\nYour prostate makes and stores seminal fluid - a milkey liquid that protects and nourishes sperm. Your prostate surrounds part of your urethra, the tube that carries urine and semon out of your body. Many men develop a noncancerous condition called bengin prostatic hyperplasia (BPH), or enlargement of the prostate. If the prostate, which is normally about the size of a walnut, grows too large, it can slow or block the flow of urine. \n\n# **Symptoms of prostate cancer**\nProstate cancer symptoms typically don't appear early in the disease. In many men, doctors first detect signs of prostate cancer during routine check-up. More advanced prostate cancer symptoms may include:\n* Weak or interrupted flow of urine\n* Urinating often (especially at night)\n* Difficulty getting or sustaining an erection (impotance)\n* Painful ejaculation\n* Frequent pain or stiffness in the lower back, hips or upper thighs\n\n# **Diagnosing prostate cancer**\nProstate cancer is curable, when it is diagnosed early. Good prostate cancer screening tests, like the prostate-specific antigen (PSA) test, have resulted in early diagnosis in about 80 percent of men with the disease. According to the American Cancer Society (ACS), all of these men survive at least five years. Whether cancer is suspected based on symptoms or a digital rectal exam or PSA test, the actual diagnosis is made with a prostate biposy, a procedure in which samples of your prostate are removed and examined under a microscope.\n\nA core needle biopsy, the main method for diagnosing prostate cancer, is typically performed in a doctor's office by a urologist as follows:\n* Using transrectal ultrasound (TRUS) and a local anesthetic, the doctor inserts a needle into your prostate through a probe in your rectum.\n* The doctor uses the needle to take about 12 samples of cells.\n* The procedure typically takes no more than 5 to 10 minutes, and you should have very little discomfort.\n\nAn imaging test called an Axumin positron emission tomography (PET) scan may assist in detecting prostate cancer that has come back in men whose PSA levels rise after they've had treatment. Before the scan, you receive an injection of fluciclovine F18 (Axumin), a radioactive agent that tends to collect in areas of cancer activity, which then light up on your scan.\n\n# **What causes prostate cancer?**\nWhile the exact cause of prostate cancer is unknown, generally speaking it results from mutations in cell DNA. DNA is the chemical that makes up your genes, which control when your cells grow, divide into new cells and die. DNA mutations that turn on oncogenes which help cells growand divide, or that turn off tumor-suppressor genes (which slow cell division or make cells die when they should) can cause prostate cells to grow abnormally and lead to cancer. \n## *Prostate cancer risk factors*\nNumerous factors may contribute to prostate cancer risk. The main risk factors (variables) are as follows:\n* Age: Although prostate cancer can occur at any age, it is most often found in men over age 50, and more than two-thirds of men diagnosed with the disease are over 65. About 6 cases in 10 are diagnosed in men who are 65 or older, and it is rare in men under 40.\n* Family history and genetics: A family history of prostate cancer may increase your risk, particularly if you have a number of close relatives who were younger than 60 when they were diagnosed. If your father or brother had prostate cancer, your risk is two to three times greater than if you had no family history of the disease. \n* Race or ethnicity: African-American men are more likely than men of other races to develop prostate according to different research conducted in this area. The disease is less common among men of Asian or Hispanic/Latino descent than among those of European descent.\n* Nationality: Prostate cancer is most common in North America, northwestern Europe, Australia and the Caribbean and less common in Asia, Africa and Central and South America. \n* Hormone levels: Research suggests that the development of prostate cancer is linked to higher levels of certain hormones, such as testosterone, the main male sex hormone. Testosterone is changed into dihydrotestostrone (DHT) by an enzyme in the body. DHT is important for normal prostate growth but can also cause the prostate to get bigger and may play a role in development of prostate cancer. \n* Diet: Scientists believe that diet is a critical factor in prostate cancer risk. A diet high in red meat, dairy foods and calcium and low in fruits and vegetables may play a part. Vitamin E and folic acid are also thought to increase the risk. "},{"metadata":{},"cell_type":"markdown","source":"# **Analysis**\nThe dataset consists of around 11,000 whole-side images (WSI) of digitized H&E-stained prostate biopsies originating from Radboud University Medical Center and the Karolinska Institute. \"isup_grade\" is the target variable which illustrats the severity of the cancer on a 0-5 scale. \"gleason_score\" is an alternative cancer severity rating system with more levels than the ISUP scale. \n"},{"metadata":{"trusted":true},"cell_type":"code","source":"import openslide\nimport skimage.io\nimport seaborn as sns\nimport matplotlib\nimport matplotlib.pyplot as plt\nimport PIL\nfrom IPython.display import Image, display\nimport plotly.graph_objs as go\nimport numpy as np\nimport pandas as pd\nimport torch.nn.functional as F\nimport os\nimport torch\nimport torch.nn as nn\nfrom torch.utils.data import Dataset,DataLoader\nfrom torchvision import transforms,models\nfrom tqdm import tqdm_notebook as tqdm\nimport math\nimport torch.utils.model_zoo as model_zoo\nimport cv2\nimport openslide\nimport skimage.io\nimport random\nfrom sklearn.metrics import cohen_kappa_score\nimport albumentations\nfrom PIL import Image\nimport os\nfrom fastai import *\nfrom fastai.vision import *\nimport openslide\nfrom PIL import Image as pil_image","execution_count":null,"outputs":[]},{"metadata":{},"cell_type":"markdown","source":"# **Importing Dataset**"},{"metadata":{"trusted":true},"cell_type":"code","source":"BASE_PATH = '../input/prostate-cancer-grade-assessment'\ndata_dir = f'{BASE_PATH}/train_images'\nmask_dir = f'{BASE_PATH}/train_label_masks'\ntrain = pd.read_csv(f'{BASE_PATH}/train.csv').set_index('image_id')\ntest = pd.read_csv(f'{BASE_PATH}/test.csv')\nsubmission = pd.read_csv(f'{BASE_PATH}/sample_submission.csv')\ndisplay(train.head())\nprint(\"Shape of training data :\", train.shape)\ndisplay(test.head())\nprint(\"Shape of training data :\", test.shape)\ntrain.isna().sum()","execution_count":null,"outputs":[]},{"metadata":{},"cell_type":"markdown","source":"# **Exploratory Data Analysis**"},{"metadata":{"trusted":true},"cell_type":"code","source":"def plot_count(df, feature, title='', size=2):\n    f, ax = plt.subplots(1,1, figsize=(4*size,3*size))\n    total = float(len(df))\n    sns.countplot(df[feature],order = df[feature].value_counts().index, palette='Set2')\n    plt.title(title)\n    for p in ax.patches:\n        height = p.get_height()\n        ax.text(p.get_x()+p.get_width()/2.,\n                height + 3,\n                '{:1.3f}%'.format(100*height/total),\n                ha=\"center\") \n    plt.show()\ndef plot_relative_distribution(df, feature, hue, title='', size=2):\n    f, ax = plt.subplots(1,1, figsize=(4*size,3*size))\n    total = float(len(df))\n    sns.countplot(x=feature, hue=hue, data=df, palette='Set2')\n    plt.title(title)\n    for p in ax.patches:\n        height = p.get_height()\n        ax.text(p.get_x()+p.get_width()/2.,\n                height + 3,\n                '{:1.2f}%'.format(100*height/total),\n                ha=\"center\") \n    plt.show()\ndef display_images(slides): \n    f, ax = plt.subplots(5,3, figsize=(18,22))\n    for i, slide in enumerate(slides):\n        image = openslide.OpenSlide(os.path.join(data_dir, f'{slide}.tiff'))\n        spacing = 1 / (float(image.properties['tiff.XResolution']) / 10000)\n        patch = image.read_region((1780,1950), 0, (256, 256))\n        ax[i//3, i%3].imshow(patch) \n        image.close()       \n        ax[i//3, i%3].axis('off')\n        \n        image_id = slide\n        data_provider = train.loc[slide, 'data_provider']\n        isup_grade = train.loc[slide, 'isup_grade']\n        gleason_score = train.loc[slide, 'gleason_score']\n        ax[i//3, i%3].set_title(f\"ID: {image_id}\\nSource: {data_provider} ISUP: {isup_grade} Gleason: {gleason_score}\")\n\n    plt.show() \nplot_count(df=train, feature='data_provider', title = 'Data Provider Frequency Percentage Plot')\nplot_count(df=train, feature='isup_grade', title = 'ISUP Grade Frequency Percentage Plot')\nplot_count(df=train, feature='gleason_score', title = 'Gleason Score Frequency Percentage Plot', size=3)\nplot_relative_distribution(df=train, feature='isup_grade', hue='data_provider', title = 'Relative Count Plot of ISUP Grade with Data Provider', size=2)\nplot_relative_distribution(df=train, feature='gleason_score', hue='data_provider', title = 'Relative Count Plot of Gleason Score with Data Provider', size=3)\nimages = [\n    '07a7ef0ba3bb0d6564a73f4f3e1c2293',\n    '037504061b9fba71ef6e24c48c6df44d',\n    '035b1edd3d1aeeffc77ce5d248a01a53',\n    '059cbf902c5e42972587c8d17d49efed',\n    '06a0cbd8fd6320ef1aa6f19342af2e68',\n    '06eda4a6faca84e84a781fee2d5f47e1',\n    '0a4b7a7499ed55c71033cefb0765e93d',\n    '0838c82917cd9af681df249264d2769c',\n    '046b35ae95374bfb48cdca8d7c83233f',\n    '074c3e01525681a275a42282cd21cbde',\n    '05abe25c883d508ecc15b6e857e59f32',\n    '05f4e9415af9fdabc19109c980daf5ad',\n    '060121a06476ef401d8a21d6567dee6d',\n    '068b0e3be4c35ea983f77accf8351cc8',\n    '08f055372c7b8a7e1df97c6586542ac8'\n]\n\ndisplay_images(images)\ndef display_masks(slides): \n    f, ax = plt.subplots(5,3, figsize=(18,22))\n    for i, slide in enumerate(slides):\n        \n        mask = openslide.OpenSlide(os.path.join(mask_dir, f'{slide}_mask.tiff'))\n        mask_data = mask.read_region((0,0), mask.level_count - 1, mask.level_dimensions[-1])\n        cmap = matplotlib.colors.ListedColormap(['black', 'gray', 'green', 'yellow', 'orange', 'red'])\n\n        ax[i//3, i%3].imshow(np.asarray(mask_data)[:,:,0], cmap=cmap, interpolation='nearest', vmin=0, vmax=5) \n        mask.close()       \n        ax[i//3, i%3].axis('off')\n        \n        image_id = slide\n        data_provider = train.loc[slide, 'data_provider']\n        isup_grade = train.loc[slide, 'isup_grade']\n        gleason_score = train.loc[slide, 'gleason_score']\n        ax[i//3, i%3].set_title(f\"ID: {image_id}\\nSource: {data_provider} ISUP: {isup_grade} Gleason: {gleason_score}\")\n        f.tight_layout()\n        \n    plt.show()\ndisplay_masks(images)","execution_count":null,"outputs":[]},{"metadata":{"trusted":true},"cell_type":"code","source":"def seed_torch(seed=42):\n    random.seed(seed)\n    os.environ['PYTHONHASHSEED'] = str(seed)\n    np.random.seed(seed)\n    torch.manual_seed(seed)\n    torch.cuda.manual_seed(seed)\n    torch.backends.cudnn.deterministic = True\nseed_torch(seed=42)\nclass config:\n    device = torch.device(\"cuda:0\" if torch.cuda.is_available() else \"cpu\")\n\n    IMG_WIDTH = 256\n    IMG_HEIGHT = 256\n    TEST_BATCH_SIZE = 1\n    CLASSES = 6","execution_count":null,"outputs":[]}],"metadata":{"kernelspec":{"language":"python","display_name":"Python 3","name":"python3"},"language_info":{"pygments_lexer":"ipython3","nbconvert_exporter":"python","version":"3.6.4","file_extension":".py","codemirror_mode":{"name":"ipython","version":3},"name":"python","mimetype":"text/x-python"}},"nbformat":4,"nbformat_minor":4}