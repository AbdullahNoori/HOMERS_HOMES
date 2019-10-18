from unittest import TestCase, main as unittest_main, mock
from flask import Flask
from app import app
from bson.objectid import ObjectId

sample_home_id = ObjectId('5d55cffc4a3d4031f42827a3')
sample_home = {
    'title': 'Home',
    'image': ''https://www.realtor.com/realestateandhomes-detail/9386-Leopard-Lily-Ct_Sacramento_CA_95829_M27808-31388,
    'price': "$541,999"
}
sample_form_data = {
    'title': sample_home['title'],
    'image': sample_home['image'],
    'price': sample_home['price']
}

class PlaylistsTests(TestCase):
    def setUp(self):
        # test setup
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_index(self):
        # test homepage."""
        result = self.client.get('/')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'home', result.data)

    def test_new(self):
        """Test the new home creation page."""
        result = self.client.get('/home/new')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'New Home', result.data)
    
    @mock.patch('pymongo.collection.Collection.find_one')
    def test_show_home(self, mock_find):
        """Test showing a single playlist."""
        mock_find.return_value = sample_home

        result = self.client.get(f'/home/{sample_home_id}')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'homes', result.data)

    @mock.patch('pymongo.collection.Collection.find_one')
    def test_edit_home(self, mock_find):
        """Test editing a single home"""
        mock_find.return_value = sample_home

        result = self.client.get(f'/homes/{sample_home_id}/edit')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'homes', result.data)

    @mock.patch('pymongo.collection.Collection.delete_one')
    def test_delete_home(self, mock_delete):
        form_data = {'_method': 'DELETE'}
        result = self.client.post(f'/home/{sample_homes_id}/delete', data=form_data)
        self.assertEqual(result.status, '302 FOUND')
        mock_delete.assert_called_with({'_id': sample_home_id})

if __name__ == '__main__':
    unittest_main()
