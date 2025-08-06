import os
from sins.sins import generate
from sins.sins import read_file
from sins.beta import beta_decay_spectrum
from sins.ec import ec_spectrum

def run_tests():
    csv_path = './Ir-192/ir-192.csv'   ### Can change test isotope here
    print(f"Testing with file: {csv_path}")

    if not os.path.isfile(csv_path):
        print(f"File does not exist: {csv_path}")
        return

    # Test read_file
    try:
        start_iso, beta_pathes, ec_pathes = read_file(csv_path)
        print("read_file: PASS")
        print(f"  start_iso: {start_iso}")
        print(f"  beta_pathes count: {len(beta_pathes)}")
        print(f"  ec_pathes count: {len(ec_pathes)}")
    except Exception as e:
        print(f"read_file: FAIL - {e}")
        return

    # Test beta_decay_spectrum if beta paths exist
    if beta_pathes:
        try:
            energies, total_beta, total_nu = beta_decay_spectrum(start_iso, beta_pathes)
            assert isinstance(energies, (list, tuple))
            assert isinstance(total_beta, (list, tuple))
            assert isinstance(total_nu, (list, tuple))
            print(f"beta_decay_spectrum: PASS - energies length: {len(energies)}")
        except Exception as e:
            print(f"beta_decay_spectrum: FAIL - {e}")
    else:
        print("beta_decay_spectrum: SKIPPED - no beta paths")

    # Test ec_spectrum if ec paths exist
    if ec_pathes:
        try:
            energies, nu_spectrum = ec_spectrum(ec_pathes)
            assert isinstance(energies, (list, tuple))
            assert isinstance(nu_spectrum, (list, tuple))
            print(f"ec_spectrum: PASS - energies length: {len(energies)}")
        except Exception as e:
            print(f"ec_spectrum: FAIL - {e}")
    else:
        print("ec_spectrum: SKIPPED - no EC paths")

    # Test generate function
    try:
        results = generate(csv_path, gen_files=False)
        print(f"generate function: PASS - returned {len(results)} outputs")
    except Exception as e:
        print(f"generate function: FAIL - {e}")

if __name__ == "__main__":
    run_tests()