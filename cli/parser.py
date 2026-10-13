import argparse

def create_parser():
    parser = argparse.ArgumentParser('BrewSec Vulnerable Web Application')
    
    parser.add_argument(
        '--vuln',
        help='Vulnerability category, e.g. sqli, xss, csrf'
    )
    
    parser.add_argument(
        '--level',
        type=int,
        help='Lab level, e.g. 1-5'
    )
    
    parser.add_argument(
        '--list',
        help='List available labs'
    )
    
    return parser