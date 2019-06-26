#!/usr/bin/env python3

import json
import subprocess
import unittest

import responses


def _mock_api_request():
    """Set a mock response from the geocode API.

    It's nice to avoid external dependencies/network requests in
    unit tests. Also Microsoft might frown upon having tests hammer
    their dev/test environment.

    TODO: All tests currently use the same mock response. It would be
    good to add tests that use different mock responses to test the
    robustness of the find_store script's API response parsing code.
    """
    with open('mock_api_response.json') as f:
        response = json.load(f)
    responses.add(responses.GET, json=response)


class FindStoreTest(unittest.TestCase):
    @responses.activate
    def test_lookup_by_zip_with_text_output(self):
        _mock_api_request()
        proc = subprocess.run(['./find_store', '--zip=27513'], capture_output=True)
        self.assertEqual(b'', proc.stderr)
        self.assertEqual(
            b'The nearest store to 27513 is the Morrisville store, ' +
            b'located at SWC NC Hwy 54 & Cary Parkway.\n' +
            b'It\'s 2.0 mi away.\n' +
            b'Address: 3001 Market Center Dr\n' +
            b'         Morrisville, NC 27560\n', proc.stdout)

    @responses.activate
    def test_json_output(self):
        _mock_api_request()
        proc = subprocess.run(
            ['./find_store', '--zip=27513', '--output=json'], capture_output=True)
        self.assertEqual(b'', proc.stderr)
        json_output = json.loads(proc.stdout)
        self.assertFalse('error' in json_output)
        self.assertEqual('Morrisville', json_output['Store Name'])
        self.assertEqual('SWC NC Hwy 54 & Cary Parkway', json_output['Store Location'])
        self.assertEqual('3001 Market Center Dr', json_output['Address'])
        self.assertEqual('Morrisville', json_output['City'])
        self.assertEqual('NC', json_output['State'])
        self.assertEqual('27560', json_output['Zip Code'])
        self.assertEqual('35.8052198', json_output['Latitude'])
        self.assertEqual('-78.8154332', json_output['Longitude'])
        self.assertEqual('Wake County', json_output['County'])
        self.assertEqual('1.9614 mi', json_output['Distance'])

    @responses.activate
    def test_lookup_by_address(self):
        _mock_api_request()
        proc = subprocess.run([
            './find_store',
            '--address="1600 Pennsylvania Ave NW, Washington, DC"',
            '--output=json'
        ], capture_output=True)
        self.assertEqual(b'', proc.stderr)
        json_output = json.loads(proc.stdout)
        self.assertFalse('error' in json_output)
        self.assertEqual('Rosslyn', json_output['Store Name'])
        self.assertEqual('2.2968 mi', json_output['Distance'])

    @responses.activate
    def test_kilometers(self):
        _mock_api_request()
        proc = subprocess.run(
            ['./find_store', '--zip=27513', '--output=json', '--units=km'], capture_output=True)
        self.assertEqual(b'', proc.stderr)
        json_output = json.loads(proc.stdout)
        self.assertFalse('error' in json_output)
        self.assertEqual('3.1563 km', json_output['Distance'])

    @responses.activate
    def test_no_geocode_results_with_text_output(self):
        _mock_api_request()
        proc = subprocess.run(
            ['./find_store', '--address=A'], capture_output=True)
        self.assertEqual(b'', proc.stdout)
        self.assertEqual(
            b'Error: Could not locate that address on a map. You ' +
            b'may wish to verify that it is correct.\n', proc.stderr)

    @responses.activate
    def test_no_geocode_results_with_json_output(self):
        _mock_api_request()
        proc = subprocess.run(
            ['./find_store', '--address=A', '--output=json'], capture_output=True)
        self.assertEqual(b'', proc.stdout)
        json_output = json.loads(proc.stderr)
        self.assertEqual(
            'Could not locate that address on a map. You ' +
            'may wish to verify that it is correct.', json_output['error'])


if __name__ == '__main__':
    unittest.main()
