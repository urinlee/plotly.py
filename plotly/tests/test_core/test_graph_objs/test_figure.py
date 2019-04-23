from __future__ import absolute_import

from unittest import TestCase

import plotly.graph_objs as go


class FigureTest(TestCase):

    def test_instantiation(self):

        native_figure = {
            'data': [],
            'layout': {},
            'frames': []
        }

        go.Figure(native_figure)
        go.Figure()

    def test_access_top_level(self):

        # Figure is special, we define top-level objects that always exist.

        self.assertEqual(go.Figure().data, ())
        self.assertEqual(go.Figure().layout.to_plotly_json(), {})
        self.assertEqual(go.Figure().frames, ())

    def test_nested_frames(self):
        with self.assertRaisesRegexp(ValueError, 'frames'):
            go.Figure({'frames': [{'frames': []}]})

        figure = go.Figure()
        figure.frames = [{}]

        with self.assertRaisesRegexp(ValueError, 'frames'):
            figure.to_plotly_json()['frames'][0]['frames'] = []
            figure.frames[0].frames = []

    def test_raises_invalid_property_name(self):
        with self.assertRaises(ValueError):
            go.Figure(
                data=[{'type': 'bar', 'bogus': 123}],
                layout={'bogus': 23, 'title': 'Figure title'},
                frames=[{
                    'data': [{'type': 'bar', 'bogus': 123}],
                    'layout': {'bogus': 23, 'title': 'Figure title'},
                }])

    def test_skip_invalid_property_name(self):
        fig = go.Figure(
            data=[{'type': 'bar', 'bogus': 123}],
            layout={'bogus': 23, 'title': {'text': 'Figure title'}},
            frames=[{
                'data': [{'type': 'bar', 'bogus': 123}],
                'layout': {'bogus': 23, 'title': 'Figure title'},
            }],
            bogus=123,
            skip_invalid=True)

        fig_dict = fig.to_dict()

        # Remove trace uid property
        for trace in fig_dict['data']:
            trace.pop('uid', None)

        self.assertEqual(fig_dict['data'],
                         [{'type': 'bar'}])
        self.assertEqual(fig_dict['layout'],
                         {'title': {'text': 'Figure title'}})
        self.assertEqual(fig_dict['frames'],
                         [{
                             'data': [{'type': 'bar'}],
                             'layout':  {'title': {'text': 'Figure title'}}
                         }])

    def test_raises_invalid_property_value(self):
        with self.assertRaises(ValueError):
            go.Figure(
                data=[{'type': 'bar', 'showlegend': 'bad_value'}],
                layout={'paper_bgcolor': 'bogus_color',
                        'title': 'Figure title'},
                frames=[{
                    'data': [{'type': 'bar', 'showlegend': 'bad_value'}],
                    'layout': {'bgcolor': 'bad_color',
                               'title': 'Figure title'},
                }])

    def test_skip_invalid_property_value(self):
        fig = go.Figure(
            data=[{'type': 'bar', 'showlegend': 'bad_value'}],
            layout={'paper_bgcolor': 'bogus_color', 'title': 'Figure title'},
            frames=[{
                'data': [{'type': 'bar', 'showlegend': 'bad_value'}],
                'layout': {'bgcolor': 'bad_color', 'title': 'Figure title'},
            }],
            skip_invalid=True,
        )

        fig_dict = fig.to_dict()

        # Remove trace uid property
        for trace in fig_dict['data']:
            trace.pop('uid', None)

        self.assertEqual(fig_dict['data'],
                         [{'type': 'bar'}])
        self.assertEqual(fig_dict['layout'],
                         {'title': {'text': 'Figure title'}})
        self.assertEqual(fig_dict['frames'],
                         [{
                             'data': [{'type': 'bar'}],
                             'layout':
                                 {'title': {'text': 'Figure title'}}
                         }])

    def test_raises_invalid_toplevel_kwarg(self):
        with self.assertRaises(TypeError):
            go.Figure(
                data=[{'type': 'bar'}],
                layout={'title': 'Figure title'},
                frames=[{
                    'data': [{'type': 'bar'}],
                    'layout': {'title': 'Figure title'},
                }],
                bogus=123
            )

    def test_toplevel_underscore_kwarg(self):
        fig = go.Figure(
            data=[{'type': 'bar'}],
            layout_title_text='Hello, Figure title!'
        )

        self.assertEqual(fig.layout.title.text, 'Hello, Figure title!')
