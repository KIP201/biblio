import unittest
import sys
import os
from tests.test_models import TestModels
from tests.test_auth import TestAuth
from tests.test_livres import TestLivres
from tests.test_amendes import TestAmendes
from tests.test_search import TestSearch
from tests.test_validations import TestValidations
from tests.test_performance import TestPerformance
from tests.test_error_handlers import TestErrorHandlers
from tests.test_api import TestAPI

def run_tests():
    # Configuration de l'environnement de test
    os.environ['FLASK_ENV'] = 'testing'
    os.environ['DATABASE_URL'] = 'sqlite:///test_db/test.db'
    
    # Création du dossier de test
    if not os.path.exists('test_db'):
        os.makedirs('test_db')
    
    # Création de la suite de tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Ajout de tous les tests
    test_cases = [
        TestModels,
        TestAuth,
        TestLivres,
        TestAmendes,
        TestSearch,
        TestValidations,
        TestPerformance,
        TestErrorHandlers,
        TestAPI
    ]
    
    for test_case in test_cases:
        suite.addTests(loader.loadTestsFromTestCase(test_case))
    
    # Exécution des tests avec couverture de code
    try:
        import coverage
        cov = coverage.Coverage()
        cov.start()
        
        # Exécution des tests
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        
        cov.stop()
        cov.save()
        
        # Rapport de couverture
        print('\nCouverture de code:')
        cov.report()
        cov.html_report(directory='coverage_report')
        
    except ImportError:
        # Si coverage n'est pas installé, exécuter les tests sans couverture
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
    
    # Nettoyage
    if os.path.exists('test_db/test.db'):
        os.remove('test_db/test.db')
    
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    sys.exit(run_tests()) 