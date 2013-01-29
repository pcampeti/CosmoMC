
import ResultObjs, sys, os, iniFile


if len(sys.argv) < 3:
    print 'Usage: python/bestFitCAMB.py chain_root iniName'
    sys.exit()

root = os.path.abspath(sys.argv[1])

pars = {'ombh2':'omegabh2', 'omch2':'omegach2', 'omnuh2':'omeganuh2', 'hubble':'H0', 'w':'w',
        'helium_fraction':'yheused', 'scalar_amp(1)':'A' , 'scalar_spectral_index(1)':'ns', 'scalar_nrun(1)':'nrun', 'initial_ratio(1)':'r',
        're_optical_depth':'tau', 're_delta_redshift':'deltazrei'}

ini = iniFile.iniFile()
nmassive = 1
ini.params['massless_neutrinos'] = 3.046 - nmassive
ini.params['massive_neutrinos'] = nmassive
ini.params['re_use_optical_depth'] = True
ini.params['temp_cmb'] = 2.7255
ini.params['CMB_outputscale'] = 2.7255e6 ** 2.
ini.params['tensor_spectral_index(1)'] = -float(ini.params['initial_ratio(1)']) / 8
ini.defaults.append('params.ini')

bf = ResultObjs.bestFit(root + '.minimum', setParamNameFile=root + '.paramnames', want_fixed=True)

for camb, cosmomc in pars.items():
    par = bf.parWithName(cosmomc)
    print camb, cosmomc, par
    if par is not None: ini.params[camb] = par.best_fit

ini.params['scalar_amp(1)'] = float(ini.params['scalar_amp(1)']) / 1e9


ini.saveFile(sys.argv[2])
